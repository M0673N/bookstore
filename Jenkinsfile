// Multibranch Pipeline with Webhook Trigger for when the GitHub Actions minutes run out

pipeline {
    agent any

    environment {
        SECRET_KEY = credentials('SECRET_KEY_BOOKSTORE')
        CLOUDINARY_NAME = credentials('CLOUDINARY_NAME_BOOKSTORE')
        EMAIL_PORT = credentials('EMAIL_PORT_BOOKSTORE')
        DOCKERHUB_TOKEN = credentials('DOCKERHUB_TOKEN')
        KOYEB_API = credentials('KOYEB_API')
        KOYEB_SERVICE_ID = credentials('KOYEB_SERVICE_ID_BOOKSTORE')
    }

    stages {
        stage('Build') {
            steps {
                // Assuming you have Python 3.10 installed
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv .venv
                            . .venv/bin/activate
                            python3 -m pip install --upgrade pip
                            pip3 install -r requirements.txt
                            pip3 install flake8
                        '''
                    } else {
                        bat '''
                            python -m venv .venv
                            call .venv/Scripts/activate
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                            pip install flake8
                        '''
                    }
                }
            }
        }

        stage('Lint') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . .venv/bin/activate
                            flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=.venv
                            flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=.venv
                        '''
                    } else {
                        bat '''
                            call .venv/Scripts/activate
                            flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=.venv
                            flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=.venv
                        '''
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . .venv/bin/activate
                            python3 manage.py test
                        '''
                    } else {
                        bat '''
                            call .venv/Scripts/activate
                            python manage.py test
                        '''
                    }
                }
            }
        }

        stage('Docker Build and Push') {
            when {
                branch 'main'
            }
            steps {
                script {
                    def version = new Date().format('dd.MM.yyyy')
                    if (isUnix()) {
                        sh """
                            echo ${env.DOCKERHUB_TOKEN} | docker login -u m0673n -p ${env.DOCKERHUB_TOKEN}
                            docker build -t m0673n/bookstore:${version} .
                            docker tag m0673n/bookstore:${version} m0673n/bookstore:latest
                            docker push m0673n/bookstore:${version}
                            docker push m0673n/bookstore:latest
                            docker logout
                        """
                    } else {
                        bat """
                            echo ${env.DOCKERHUB_TOKEN} | docker login -u m0673n -p ${env.DOCKERHUB_TOKEN}
                            docker build -t m0673n/bookstore:${version} .
                            docker tag m0673n/bookstore:${version} m0673n/bookstore:latest
                            docker push m0673n/bookstore:${version}
                            docker push m0673n/bookstore:latest
                            docker logout
                        """
                    }
                }
            }
        }
        stage('Deploy to Koyeb') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Trigger redeploy via the Koyeb API
                    if (isUnix()) {
                        sh """
                            curl -X POST \
                            https://app.koyeb.com/v1/services/$KOYEB_SERVICE_ID/redeploy \
                            -H 'Authorization: Bearer $KOYEB_API'
                        """
                    } else {
                        bat '''
                            curl -X POST ^
                            "https://app.koyeb.com/v1/services/%KOYEB_SERVICE_ID%/redeploy" ^
                            -H "Authorization: Bearer %KOYEB_API%"
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs() // Clean workspace after the build
        }
    }
}
