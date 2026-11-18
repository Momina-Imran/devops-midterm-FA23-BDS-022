pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    triggers { githubPush() }

    environment {
        IMAGE     = 'midterm-api'
        CONTAINER = 'midterm-api'
        PUBLIC_IP = '16.176.42.254'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Train & Build Image') {
            steps {
                sh '''
                    GIT_SHA=$(git rev-parse HEAD)
                    docker build --build-arg GIT_COMMIT=$GIT_SHA -t $IMAGE:latest .
                '''
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm $IMAGE:latest python -m pytest -q'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f $CONTAINER || true
                    docker run -d --name $CONTAINER --restart unless-stopped -p 8000:8000 $IMAGE:latest
                    for i in $(seq 1 30); do
                        if curl -fs http://localhost:8000/metrics; then echo; exit 0; fi
                        sleep 2
                    done
                    docker logs $CONTAINER
                    exit 1
                '''
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
            emailext(
                from: 'mominaimran478@gmail.com',
                to: 'qasimalik@gmail.com',
                subject: "FA23-BDS-022 | MIDTERM pipeline ${currentBuild.currentResult} | Build #${env.BUILD_NUMBER}",
                body: """Student Reg No: FA23-BDS-022
Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Result: ${currentBuild.currentResult}
Commit: ${env.GIT_COMMIT}
Metrics: http://${env.PUBLIC_IP}:8000/metrics
Build log: ${env.BUILD_URL}
"""
            )
        }
    }
}