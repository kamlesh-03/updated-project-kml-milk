pipeline {
  agent any

  environment {
    IMAGE = "DOCKERHUB_USERNAME/kml-milk"
    NAMESPACE = "kml-milk"
    APP_NAME = "kml-milk"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Python Test') {
      steps {
        sh '''
          python3 -m venv .ci-venv
          . .ci-venv/bin/activate
          pip install -r requirements.txt
          python manage.py check
          python manage.py test
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t ${IMAGE}:${BUILD_NUMBER} -t ${IMAGE}:latest .'
      }
    }

    stage('Push Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push ${IMAGE}:${BUILD_NUMBER}
            docker push ${IMAGE}:latest
            docker logout
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        sh '''
          sed "s#DOCKERHUB_USERNAME/kml-milk:BUILD_NUMBER#${IMAGE}:${BUILD_NUMBER}#g" k8s/deployment.yaml > /tmp/deployment.yaml
          kubectl apply -f k8s/namespace.yaml
          kubectl apply -f /tmp/deployment.yaml
          kubectl apply -f k8s/service.yaml
          kubectl rollout status deployment/${APP_NAME} -n ${NAMESPACE} --timeout=180s
        '''
      }
    }
  }

  post {
    always {
      sh 'docker image prune -f || true'
    }
    success {
      echo 'KML Milk CI/CD completed successfully.'
    }
  }
}
