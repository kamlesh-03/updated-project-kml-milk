pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'kmlraut/kml-milk'
        KUBECONFIG   = '/var/lib/jenkins/.kube/config'

    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} -t ${DOCKER_IMAGE}:latest .
                '''
            }
        }

        stage('Test Container') {
            steps {
                sh '''
                    docker rm -f kml-milk-dairy-test || true
                    docker run -d --name kml-milk-dairy-test -p 8082:8000 ${DOCKER_IMAGE}:${BUILD_NUMBER}
                    
                    # Allow 8 seconds for Django/Gunicorn to start up
                    sleep 8
                    
                    # Test root endpoint or /health/ endpoint
                    curl -f http://localhost:8082 || curl -f http://localhost:8082/health/
                    
                    # Clean up test container
                    docker rm -f kml-milk-dairy-test
                '''
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'kmlraut-credential',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    echo "Deploying dairy-deploy to Kubernetes..."
                    
                    # Update deployment image
                    kubectl set image deployment/dairy-deploy \
                        dairy-deploy=${DOCKER_IMAGE}:${BUILD_NUMBER}
                    
                    # Monitor rollout
                    kubectl rollout status deployment/dairy-deploy --timeout=60s
                    
                    echo "Kubernetes deployment successful!"
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f kml-milk-dairy-test || true'
        }
        success {
            echo 'CI/CD Pipeline completed successfully!'
        }
        failure {
            echo 'CI/CD Pipeline failed!'
        }
    }
}