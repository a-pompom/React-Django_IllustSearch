from .messages_custom_type import TypeMessages

# アプリで利用するメッセージ管理用ディクショナリ
messages: TypeMessages = {
    'common': {
        'success': {
            'response_ok': 'ok'
        },
        'error': {
            'unauthorized': 'unauthorized...',
            'update_failure': '登録に失敗しました。'
        }
    },
    'category': {
        'error': {
            'update': {
                'invalid_uuid': 'カテゴリIDはUUID形式で指定してください。',
                'not_found': '更新対象のカテゴリが見つかりませんでした。',
            },
            'delete': {
                'invalid_uuid': 'カテゴリIDはUUID形式で指定してください。',
                'not_found': '削除対象のカテゴリが見つかりませんでした。',
            }
        }

    },
}