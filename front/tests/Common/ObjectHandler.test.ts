import { getPropertyByKeyString } from 'Common/objectHandler';

describe('ネストしたオブジェクト内のプロパティをキー文字列で取得', () => {

    test('一段階のネストしたオブジェクトを取得できること。', () => {

        const sut = {
            user: {
                userName: 'John Doe'
            }
        }

        const result = getPropertyByKeyString(sut, 'user.userName');

        expect(result).not.toBe(null);
        expect(result).toBe('John Doe');
    });

    test.each([
        [
            {
                list:[
                    'List Item'
                ]

            },
            'list[0]',
            'List Item',
            '単一の配列'
        ],
        [
            {
                list:[
                    {
                        user1: 
                        {
                            userName: '匿名ユーザ',
                            password: 'Strong Password'
                        }
                    },
                    {
                        user2: 
                        {
                            userName: '匿名ユーザ2',
                            password: 'Strong Password2'
                        }
                    }
                ]
            },
            'list[1].user2.password',
            'Strong Password2',
            '配列を含むネストしたオブジェクト'
        ]
    ])('配列を含むネストしたオブジェクトを取得できること。', (sut, key: string, expected: string, _) => {

        const actual = getPropertyByKeyString(sut, key);

        expect(actual).toBe(expected);

    });
});