<p align="center"> 
    <img src="https://img.shields.io/github/issues/Simonko-912/mail2.0" alt="Issues">
    <img src="https://img.shields.io/github/forks/Simonko-912/mail2.0" alt="Forks">
    <img src="https://img.shields.io/github/stars/Simonko-912/mail2.0" alt="Stars">
    <img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License (GPLv3)">
    <img src="https://img.shields.io/badge/version-1.0.1-blue" alt="Version">
    <img src="https://img.shields.io/badge/contributors-0-orange" alt="Contributors">
    <img src="https://img.shields.io/github/downloads/Simonko-912/mail2.0/total" alt="Downloads">
    <img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status">
</p>




# Table of contents.
- [Basic Info](#basic-info)
- [How to set up?](#how-to-set-up)
- [How to Pick a Mail2.0 Address?](#how-to-pick-a-mail20-address)
- [Notes](#notes)

# Basic info

**Mail 2.0** is a simple mail service that uses Python for the backend and HTML for frontend. All required things are in the `requirements.txt`. 
The `runtime.txt` is the version of python that I tested and works. The `test.db` that shows after runing is the database of the server. By deleting you delete all accounts and mail. It was inspired by [Gmail](https://gmail.com/) and [Proton mail](https://mail.proton.me/). The messages are sent using JSON in this format:

```
{
  "to_email": "target@domain",
  "subject": "This is not encripted.",
  "message": "QW5kIHRoaXMgaXMgZW5jcmlwdGVkLg==" #This says "And this is encripted."
}
```
(It is not "encription" look at [Notes](#notes) for more)

The encription is just a simple Base64 for simplicity. (Still you are probably gonna use HTTPS what has encription built in)
To see all releases go to [https://github.com/Simonko-912/mail2.0/releases](https://github.com/Simonko-912/mail2.0/releases)
# How to set up?

## First clone mail2.0

```
git clone https://github.com/Simonko-912/mail2.0.git
cd mail2.0
```

### Optional: Set up venv

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

## Download Requirements

```
pip install -r requirements.txt
```

## Edit the port
Edit the port to your needs in `server.py` (In the last few lines, defult at 0.0.0.0 at port 10000) and then pick a domain or ip that you want your users to use in the `DOMAIN` variable.


## Lastly Run

```
python3 server.py
```

# How to Pick a Mail2.0 Address?
Just write `any@ip` any you can have any like `bob@ip` and the ip is the ip or domain of a server so example `bob@example.com` or `bob@111.111.11.111`

# Notes:
- This email program does not have encription, only encoding using base64. But it saves passwords with using `bcrypt` by hashing. Thats why its recomended to use HTTPS.


