pipeline {
    agent any
    environment {
        DB_SERVER = 'EPKZALMW004A'
        DB_PORT='1433'
        DB_NAME='AdventureWorks2012'
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
                sudo dnf install unixODBC
                python3 -m pip install pyodbc
                python3 -m pip install -r requirements.txt
                '''
            }
        }
        stage ('Test'){
            steps {
                withCredentials([usernamePassword(credentialsId: 'mssql_creds', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASSWORD')]) {
                sh '''
                . .venv/bin/activate
                export DB_USER=$DB_USER
                export DB_PASSWORD=$DB_PASSWORD
                pytest tests.py --html=report.html --capture=sys -rP
                '''
                }
            }
        }
    }
}