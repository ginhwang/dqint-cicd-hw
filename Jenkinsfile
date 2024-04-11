pipeline {
    agent any
    environment {
        DB_SERVER = 'myserver'
        DB_PORT = 'myport'
        DB_NAME = 'mydbname'
    }
    stages {
        stage ('GIT Checkout'){
            steps {
                git branch: 'main', url: 'https://github.com/ginhwang/dqint-cicd-hw.git'
            }
        }
        stage('build') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                python3 -m pip install -r requirements.txt
                '''
            }
        }
        stage ('Test'){
            steps {
                withCredentials([usernamePassword(credentialsId: 'mssql_creds', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASSWORD')]) {
                    sh '''
                    . .venv/bin/activate
                    pytest tests.py --html=report.html --capture=sys -rP
                    '''
                }
            }
        }
    }
}