pipeline {
    agent any
    stages {
        stage('SCM') {
            steps {
                 git branch: 'master', credentialsId: 'github', url: 'git@github.com:GeovRodri/bsi_simulador_previdencia.git'
            }
        }

        stage('Build') {
            steps {
				echo 'Building'
            }
        }

        stage('SonarQube analysis') {
            steps {
				echo 'Running code analysis'
                sh 'gradlew.bat -b build.gradle.sonarqube sonarqube'
            }
        }

        stage('Deploy') {
            steps {
				echo 'Deploying'
                sh 'docker-compose up -d'
            }
        }
    }
}