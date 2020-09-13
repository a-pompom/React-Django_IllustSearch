import { Field } from 'Common/Field';
import { Phase } from 'Common/Phase';
import { Message } from 'message.properties';

import { executeValidate } from 'Component/Signup/validator';
import * as SignupData from 'Component/Signup/signupData';

describe('ユーザ登録Validator', () => {

    // 検証対象のユーザ名情報を取得
    const getUsernameArgs = (usernameValue: string) => {
        const field: Field<SignupData.FieldName, SignupData.Value> = new Field('username', '', 'ユーザ名');
        const value: SignupData.Value = usernameValue;
        const state: SignupData.State = {
            phase: new Phase('IDLE'),
            username: field
        };

        return {
            state,
            field,
            value
        }
    };

    test('最大文字数制限を満たすユーザ名にバリデーション処理を適用すると、resultのエラーが空となること', () => {

        // GIVEN
        const usernameValue = 'a-pompom';
        const {state, field, value} = getUsernameArgs(usernameValue);

        // WHEN
        const result = executeValidate(state, field, value);

        // THEN
        expect(result[0].isValid).toBe(true);
        expect(result[0].errors.length).toBe(0);
        expect(result[0].fieldName).toBe('username');
        expect(result[0].fieldValue).toBe(usernameValue);
    });

    test('最大文字数制限を超過するユーザ名にバリデーション処理を適用すると、resultsへエラーメッセージが格納されること', () => {

        // GIVEN
        let usernameValue = '';
        for (let i=0; i < 256; i++) {
            usernameValue += 'x';
        }
        const { state, field, value } = getUsernameArgs(usernameValue);

        // WHEN
        const result = executeValidate(state, field, value);

        // THEN
        expect(usernameValue.length).toBe(256);
        expect(result[0].isValid).toBe(false);
        expect(result[0].errors.length).not.toBe(0);
        expect(result[0].errors[0]).toBe(Message.Signup.MaxLength);
    });
});