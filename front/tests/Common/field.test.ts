import * as BaseData from 'Common/BaseData';
import { Field } from 'Common/Field';

describe('Field name,value,errors属性が取得でき、バリデーション結果が得られるか検証', () => {

    // GIVEN
    // Field用の型
    type FieldName = 'user.username';
    type Value = string;
    type UsernameField<UsernameFieldName extends FieldName, UsernameValue extends Value> = Field<UsernameFieldName, UsernameValue>

    // Fieldの属性値を格納したオブジェクト
    type UserInfo = {
        name: FieldName,
        value: Value,
        label: string
    };
    const userInfo: UserInfo = {
        name: 'user.username',
        value: 'userValue',
        label: 'ユーザ名'
    };

    test('コンストラクタで対応した属性へ属性値が格納されること', () => {

        // GIVEN
        const field: UsernameField<'user.username', string> = new Field<'user.username', string>(userInfo.name, userInfo.value, userInfo.label);
        
        // THEN
        expect(field.name).toBe(userInfo.name);
        expect(field.value).toBe(userInfo.value);
        expect(field.label).toBe(userInfo.label);
        expect(field.errors.length).toBe(0);
    });

    test('getValidationResultでバリデーション結果オブジェクトが得られること', () => {

        // GIVEN
        const errorMessage = 'ユーザ名は10文字以上で入力してください。'
        const expected: BaseData.ValidationResult<FieldName, Value> = {
            isValid: false,
            fieldName: userInfo.name,
            fieldValue: userInfo.value,
            errors: [errorMessage]
        };

        const field: UsernameField<'user.username', string> = new Field<'user.username', string>(userInfo.name, userInfo.value, userInfo.label);
        field.errors.push(errorMessage);

        // WHEN
        const actual = field.getValidationResult();

        // THEN
        expect(actual).toMatchObject(expected);
    });
});