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
    stage('test') {
      steps {
        echo 'test stage'
      }
    }
    stage('build') {
      steps {
        echo 'build stage'
      }
    }
    stage('docker build') {
      steps {
        echo 'docker build stage'
      }
    }
  }
}