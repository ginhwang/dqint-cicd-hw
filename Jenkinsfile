pipeline {
    agent any
    environment {
        DB_HOST = '192.168.100.129'
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
                export DB_HOST=$DB_HOST
                export DB_PORT=$DB_PORT
                export DB_NAME=$DB_NAME
                pytest tests.py --html=report.html --capture=sys -rP
                '''
                }
            }
        }
        stage ('Push'){
            steps {
                withCredentials([usernamePassword(credentialsId: 'gituser', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_PASSWORD')]) {
                sh '''
                . .venv/bin/activate
                git config --global user.email "rhwang247@gmail.com"
                git config --global user.name "ginhwang"
                git add .
                git commit -m "Update from Jenkins CI"
                git push https://${GITHUB_USER}:${GITHUB_PASSWORD}@github.com/dqint-cicd-hw.git
                '''
                }
            }
        }
        stage ('Deploy'){
            steps {
                withCredentials([usernamePassword(credentialsId: 'b3642856-78fc-4031-b2a5-318ecfa6effb', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_PASSWORD')]) {
                    sh '''
                    . .venv/bin/activate
                    git checkout -b cd_release
                    git push https://${GITHUB_USER}:${GITHUB_PASSWORD}@github.com/dqint-cicd-hw.git cd_release
                    '''
                }
            }
        }
    }
}