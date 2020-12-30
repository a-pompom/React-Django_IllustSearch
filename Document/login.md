# ログイン画面

![image](https://user-images.githubusercontent.com/43694794/103337421-a2c51a00-4abe-11eb-9bea-c17906177874.png)


## 機能概要

### ユーザ一覧表示

画面表示の際、登録済みユーザの一覧を表示。
ログインを簡略化するため、ユーザアイコンをクリックすることでもログイン可能。

### ログイン

ユーザ名を入力し、ログインボタンを押下すると発火。
入力されたユーザ名がデータベース上に存在するものであった場合は、ログイン成功。
イラスト一覧画面へ遷移。

### ユーザ登録画面遷移

ユーザ追加を意味する「+」ボタンを押下すると発火。
ユーザ登録画面へ遷移。


## API

<details>
<summary>ユーザ一覧(GET: /login)</summary>

# List User

ログインユーザ一覧を取得。

**URL** : `/login/`

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None


## Success Response

**Condition** : 

**Code** : `200 OK`

**Content example**

```json
{
    "body": {
        "users": [
            {
                "username": "user"
            }
        ]
    }
}
```
</details>

<details>
<summary>ログイン(POST: /login)</summary>

# Login

ログイン処理を実行。

**URL** : `/login/`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None


## Success Response

**Condition** : 

**Code** : `200 OK`

**Content example**

```json
{
    "body": {
        "message": "ログイン成功。"
    }
}
```

## Error Responses

**Condition** : ユーザ名で対応するユーザが存在しない

**Code** : `401 Unauthorized`

**Content example**

```json
{
    "body": {
        "message": "ログインに失敗しました。"
    },
    "errors": [
        {
            "fieldName": "username",
            "message": "ユーザ名が間違っています。"
        }
    ]
}
```
</details>