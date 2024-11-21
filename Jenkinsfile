def alljob = JOB_NAME.tokenize('/') as String[]
def proj_name = alljob[1] //to capture a simple pipeline project name inside a manually created folder

def pushImage(image){
  image.push()
  image.push(BUILD_ID)
}

pipeline {
  environment {
    registry = "docker.somko.be"
    registryCredential = 'docker-jenkins'
    somkoNameSpace = "somko/"
  }
  agent any
  stages {
    stage('Build image') {
      when {
        branch 'master'
      }
      steps {
        script {
          docker.withRegistry("https://" + registry, registryCredential) {
            try {
              pushImage(docker.build(proj_name + "/odoo", '--pull .'))
            }
            catch(err) {
              pushImage(docker.build(somkoNameSpace + proj_name, '--pull .'))
            }
          }
        }
      }
    }
  }
}
