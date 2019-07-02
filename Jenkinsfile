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

        stage('Sonarqube') {
            environment {
                scannerHome = tool 'SonarQubeScanner'
            }
            steps {
                sh "nosetests -sv --with-xunit --xunit-file=nosetests.xml --with-xcoverage --xcoverage-file=coverage.xml"

                withSonarQubeEnv('sonarqube') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
                // timeout(time: 10, unit: 'MINUTES') {
                //     waitForQualityGate abortPipeline: true
                // }
            }
        }

        stage('Deploy') {
            steps {
				echo 'Deploying'
            }
        }
    }
}