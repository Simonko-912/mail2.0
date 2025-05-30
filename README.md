<p align="center"> 
    <img src="https://img.shields.io/github/issues/Simonko-912/mail2.0" alt="Issues">
    <img src="https://img.shields.io/github/forks/Simonko-912/mail2.0" alt="Forks">
    <img src="https://img.shields.io/github/stars/Simonko-912/mail2.0" alt="Stars">
    <img src="https://img.shields.io/github/license/Simonko-912/mail2.0" alt="License (MIT)">
    <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="Version">
    <img src="https://img.shields.io/badge/contributors-0-orange" alt="Contributors">
    <img src="https://img.shields.io/github/downloads/Simonko-912/mail2.0/total" alt="Downloads">
    <img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status">
</p>

**Mail 2.0** is a simple mail service that uses Python for the backend and HTML for frontend. All required things are in the `requirements.txt`. 
The `runtime.txt` is the version of python that I tested and works. The `test.db` that shows after runing is the database of the server. By deleting you delete all accounts and mail. It was inspired by [Gmail](https://gmail.com/) and [Proton mail](https://mail.proton.me/). The messages are sent using JSON in this format:

```
{
  "to_email": "target@domain",
  "subject": "This is not encripted.",
  "message": "QW5kIHRoaXMgaXMgZW5jcmlwdGVkLg==" #This says "And this is encripted."
}
```

The encription is just a simple Base64 for simplicity. (Still you are probably gonna use HTTPS what has encription built in)

# How to pick a mail2.0 adress?
Just write `any@ip` any you can have any like `bob@ip` and the ip is the ip or domain of a server so example `bob@example.com` or `bob@111.111.11.111`
