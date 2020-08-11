/**
 * オブジェクトのプロパティに文字列形式のキーからアクセス
 * 
 * @param target プロパティを取得する対象のオブジェクト
 * @param key オブジェクトのキー文字列
 */
export const getPropertyByKeyString = <Origin>(origin: Origin, key: string): unknown => {

    let target = origin;

    // keyのstringをループで処理
    let keyFragment = '';
    let index = -1;
    for (let i = 0; i < key.length; i++) {

        // 配列形式となっているオブジェクトを取得
        if (key[i] === '[') {
            target = target[keyFragment];
            keyFragment = '';
            continue;
        }
        // 配列をインデックスで参照
        if (key[i] === ']') {
            index = parseInt(keyFragment, 10);
            target = target[index];
            keyFragment = '';
            // obj[0].valueのように表記されているので、「.」を読み飛ばす 末尾の場合はそのままループを抜ける
            i++;
            continue;
        }

        // オブジェクトを取得
        if (key[i] === '.') {
            target = target[keyFragment];
            keyFragment = '';
            continue;
        }
        keyFragment += key[i];
    }

    // 末尾が配列表記でなかった場合、末尾のオブジェクトは読み出していないので、ここで読みだす
    if (keyFragment !== '') {
        target = target[keyFragment];
    }

    return target;
};