pipeline {
    agent any
    stages {
        stage ('GIT Checkout'){
            steps {
                git branch: 'main', url: 'https://github.com/ginhwang/dqint-cicd-hw.git'
            }
        }
        stage('build') {
            steps {
                withCredentials([file(credentialsId: 'my-env-file', variable: 'ENV_FILE')]) {
                    sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    export $(cat $ENV_FILE | xargs)
                    python3 -m pip install -r requirements.txt
                    '''
                }
            }
        }
        stage ('Test'){
            steps {
                withCredentials([file(credentialsId: 'my-env-file', variable: 'ENV_FILE')]) {
                    sh '''
                    . .venv/bin/activate
                    export $(cat $ENV_FILE | xargs)
                    pytest tests.py --html=report.html --capture=sys -rP
                    '''
                }
            }
        }
    }
}