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
                sh 'docker-compose run -d redis'
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
            sh 'docker-compose rm --force redis'
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
