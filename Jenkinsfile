// Multibranch Pipeline with Webhook Trigger for when the GitHub Actions minutes run out

pipeline {
    agent any

    environment {
        SECRET_KEY = credentials('SECRET_KEY_BOOKSTORE')
        CLOUDINARY_NAME = credentials('CLOUDINARY_NAME_BOOKSTORE')
        EMAIL_PORT = credentials('EMAIL_PORT')
        DOCKERHUB_TOKEN = credentials('DOCKERHUB_TOKEN')
        KOYEB_API = credentials('KOYEB_API')
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

        stage('Parallel') {
            // when {
            //     branch 'main'
            // }
            parallel {
                stage('Deploy to Koyeb') {
                    steps {
                        script {
                            // Define the URL for the Koyeb CLI executable
                            def koyebCliUrl = 'https://github.com/koyeb/koyeb-cli/releases/latest/download/koyeb-cli-windows-x86_64.exe'

                            // Download the Koyeb CLI executable
                            if (isUnix()) {
                                sh """
                                    curl -L -o koyeb.exe ${koyebCliUrl}
                                    chmod +x koyeb.exe  // Make it executable
                                """
                            } else {
                                bat """
                                    curl -L -o koyeb.exe ${koyebCliUrl}
                                """
                            }

                            // Run the Koyeb CLI command to redeploy the app
                            if (isUnix()) {
                                sh """
                                    ./koyeb.exe service redeploy bookstore/bookstore --token $KOYEB_API
                                """
                            } else {
                                bat '''
                                    koyeb.exe service redeploy bookstore/bookstore --token %KOYEB_API%
                                '''
                            }
                        }
                    }
                }

                stage('Docker Build and Push') {
                    steps {
                        script {
                            def version = new Date().format('dd.MM.yyyy')
                            if (isUnix()) {
                                sh """
                                    echo $DOCKERHUB_TOKEN | docker login -u m0673n -p $DOCKERHUB_TOKEN
                                    docker build -t m0673n/bookstore:${version} .
                                    docker tag m0673n/bookstore:${version} m0673n/bookstore:latest
                                    docker push m0673n/bookstore:${version}
                                    docker push m0673n/bookstore:latest
                                    docker logout
                                """
                            } else {
                                bat """
                                    echo $DOCKERHUB_TOKEN | docker login -u m0673n -p $DOCKERHUB_TOKEN
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
            }
        }
    }

    post {
        always {
            cleanWs() // Clean workspace after the build
        }
    }
}
