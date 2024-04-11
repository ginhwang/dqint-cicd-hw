pipeline {
    agent any
    stages {
        stage ('GIT Checkout'){
            steps {
                git branch: 'main', url: 'https://github.com/abcdefg/dqint-cicd-hw.git'
            }
        }
        stage('build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage ('Test'){
            steps {
                sh 'pytest tests.py --html=report.html --capture sys -rP'
            }
        }
    }
}