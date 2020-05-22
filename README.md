# AWS Secrets Manager Git Credential Helper

Please configure git like in the following example, replacing "example.com", "us-east-1", and "accounts/github" as appropriate.
~~~
git config --global credential.https://example.com.helper "! $(realpath secretsmanager-git-credential-helper.py) https://example.com"

# custom config vars
git config --global aws-secrets-manager.https://example.com.region-name "us-east-1"
git config --global aws-secrets-manager.https://example.com.secret-id "accounts/github"
~~~

Store the git credentials in a JSON object with keys "username" and "password".
