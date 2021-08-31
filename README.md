# Welcome to the README file for integrating Bitbucket with Document360.

This is Proof of Concept project which reflects any changes made to the Bitbucket repository in Document360 Dashboard.

This POC transfers any canges made to README file hosted at https://ticktock11-admin@bitbucket.org/sample_workspace_id/doc360roject.git

Any commits made to this file will be transferred to Document360 Dashboard.

Using separator (in POC separator text is "DEVELOPER_SPECIFIC"), the README file is segregated so one part is visible only to the public reader group while other part is visible to private reader group.

The integration is done using RESTful APIs of Document360 and Bitbucket.
Automation is achieved via using webhook.

File Details:
bitbucket_resource.py - contains class & methods for using bitbucket APIs
doc360_resource.py - contains class & methods for using Document360 APIs
run_process.py - this file contains function to use the APIs of Document360 & Bibucket to transfer any change made to Bitbucket repository to Document360
main.py - this file contains the webhook creation and execution of code when webhook is hit


Regards,
Shounak Deshpande
shounak.python@gmail.com
