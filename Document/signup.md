# ユーザ登録画面

![image](https://user-images.githubusercontent.com/43694794/103334161-bf0f8980-4ab3-11eb-860a-a0a6009165ee.png)

## 機能概要

イラスト資料閲覧用ユーザを新規作成。
今回は、公開することを想定していないので、入力チェックは、重複判定のみを実行。


## API

<details>
<summary>ユーザ重複チェック(POST: /login/validate/user)</summary>

# IsUserDuplicated

**URL** : `/login/validate/user`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None


## Success Response

**Condition** : ユーザ名の重複なし

**Code** : `200 OK`

**Content example**

```json
{
    "body": {
        "message": "OK"
    }
}
```

## Error Responses

**Condition** : ユーザが既に登録済み

**Code** : `422 Unprocessable Entity`

**Content example**

```json
{
    "body": {
        "message": "error"
    },
    "errors": [
        {
            "fieldName": "username",
            "message": "ユーザ名は既に使用されています。"
        }
    ]
}
```
</details>


<details>
<summary>ユーザ登録(POST: /login/signup)</summary>

# Signup

**URL** : `/login/signup`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None


## Success Response

**Condition** : ユーザ名の重複なし

**Code** : `200 OK`

**Content example**

```json
{
    "body": {
        "message": "登録しました。"
    }
}
```
</details>