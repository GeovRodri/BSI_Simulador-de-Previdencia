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
            // requires SonarQube Scanner for Gradle 2.1+
            // It's important to add --info because of SONARJNKNS-281
            steps {
				echo 'Running code analysis'
                bat 'gradlew.bat -b build.gradle.sonarqube sonarqube'
            }
        }

        stage('Deploy') {
            steps {
				echo 'Deploying'
                bat 'docker-compose up -d'
            }
        }
    }
}