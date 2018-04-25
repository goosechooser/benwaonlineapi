pipeline {
    agent any
    stages {
        stage('Build image') {
            steps {
                sh 'find . -name "*.pyc" -delete'
                sh 'mkdir work_dir'
                sh 'docker-compose build testing'
            }
        }

        stage('Test image') {
            steps {
                sh 'docker run -d -p 6379 --network=jenkins-testing redis:alpine'
                sh 'CID=$(docker ps --latest --quiet)'
                sh 'docker-compose run testing'
                sh 'sed "s/\\/testing\\///" work_dir/coverage.xml > coverage.xml'

                step([$class: 'CoberturaPublisher', autoUpdateHealth: false,
                autoUpdateStability: false, coberturaReportFile: 'coverage.xml',
                failNoReports: false, failUnhealthy: false, failUnstable: false,
                maxNumberOfBuilds: 0, onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false])
            }
        }

    }
    post {
        always {
            sh 'docker rm --force $CID'
            sh 'rm -rf work_dir'
        }
        success {
            echo 'I succeeeded!'
        }
        unstable {
            echo 'I am unstable :/'
        }
        failure {
            echo 'I failed :('
            sh 'rm -rf work_dir'
        }
        changed {
            echo 'Things were different before...'
        }
    }
}
