pipeline {
    agent any
    environment {
        DB_SERVER = EPKZALMW004A
        DB_PORT=1433
        DB_NAME=AdventureWorks2012
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