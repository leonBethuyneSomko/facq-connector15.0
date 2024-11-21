def alljob = JOB_NAME.tokenize('/') as String[]
def proj_name = alljob[1] //to capture a simple pipeline project name inside a manually created folder

def pushImage(image){
  image.push()
  image.push(env.BRANCH_NAME.replace("/", "_") + '_' + BUILD_ID)
  image.push(env.BRANCH_NAME.replace("/", "_"))
}

@NonCPS
def commitHashForBuild( build ) {
  def scmAction = build?.actions.find { action -> action instanceof jenkins.scm.api.SCMRevisionAction }
  return scmAction?.revision?.hash
}

def getLastSuccessfulCommit() {
  def lastSuccessfulHash = null
  def lastSuccessfulBuild = currentBuild.rawBuild.getPreviousSuccessfulBuild()
  if ( lastSuccessfulBuild ) {
    lastSuccessfulHash = commitHashForBuild( lastSuccessfulBuild )
  }
  return lastSuccessfulHash
}

pipeline {
  environment {
    registry = "docker.somko.be"
    registryCredential = 'docker-jenkins'
  }
  parameters {
      booleanParam(name: 'updateTest', defaultValue: false, description:'Update or Create the test environment')
    }
  agent any
  stages {
    stage('Build image') {
      steps {
        script {
          docker.withRegistry("https://" + registry, registryCredential) {
            pushImage(docker.build(proj_name + "/odoo", '--pull .'))
          }
        }
      }
    }
    stage('Update test') {
      when {
         expression { params.updateTest }
      }
      steps {
        script {
          def lastSuccessfulCommit = getLastSuccessfulCommit()
          def modules = sh(returnStdout: true, script: "git diff --dirstat --name-only --diff-filter=M " + lastSuccessfulCommit + " | grep -o -E '^.*/.*/' | cut -d'/' -f2 | sort -u | xargs | sed -e 's/ /,/g'").trim()
          def response = httpRequest 'https://s2.somko.be/update/' + proj_name + '/' + env.BRANCH_NAME.replace("/", "_") + (modules ? ("/" + modules) : "") + '?key=6IZsQKgTiyJkKQS0hKfXCnTcPumhOKEz'
          println(response.content)
        }
      }
    }
  }
}
