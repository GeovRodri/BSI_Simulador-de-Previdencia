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

        stage('Depedencies') {
            steps {
                sh "apt install libmysqlclient-dev"
				sh "pip3 install -r requirements.txt"
				sh "nosetests -sv --with-xunit --xunit-file=nosetests.xml --with-xcoverage --xcoverage-file=coverage.xml"
            }
        }

        stage('Sonarqube') {
            environment {
                scannerHome = tool 'SonarQubeScanner'
            }
            steps {
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