pipeline {
  agent any
  stages {
    stage('prepare') {
      steps {
        git credentialsId: 'soRan0219', 
            branch: 'master', 
            url: 'https://github.com/soRan0219/mcp-map-server.git'
      }
    }
    stage('build') {
      steps {
        echo 'build stage'
      }
    }
    stage('test') {
      steps {
        echo 'test stage'
        sh 'poetry run python tests/test.py'
      }
    }
    stage('deploy') {
      steps {
        echo 'deploy stage'
        sh 'docker-compose down || true'
        sh 'docker-compose up --build -d'
      }
    }
  }
}