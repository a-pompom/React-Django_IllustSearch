import * as validator from 'Common/TextValidator';

import { Field } from 'Common/Field';

describe('最小桁数チェック', () => {

    test.each([
        [new Field('', '10length..', ''), '10文字丁度'],
        [new Field('', '10lengthstr', ''), '11文字'],
        [new Field('', '10文字の日本語文字', ''), '10文字の日本語文字']

    ])('最小桁数を満たしていれば、エラーとならないこと。', (field: Field<any>, _) => {

        const minLength = 10;
        validator.validateMinLength(field, minLength);

        expect(field.errors.length).toBe(0);
    });
    test.each([
        [new Field('', '', '文字'), '0文字'],
        [new Field('', '7length', '文字'), '7文字'],
        [new Field('', '9lengthst', '文字'), '9文字']

    ])('文字数が指定桁数に満たない場合エラーとなること。', (field: Field<any>, _) => {

        const minLength = 10;
        validator.validateMinLength(field, minLength);

        expect(field.errors.length).toBe(1);
        expect(field.errors[0]).toBe(`${field.label}は${minLength}文字以上で入力してください。`);
    });

});
describe('最大桁数チェック', () => {

    test.each([
        [new Field('', '', '文字'), '0文字'],
        [new Field('', '7length', '文字'), '7文字'],
        [new Field('', '9lengthst', '文字'), '9文字']

    ])('最大桁数制約を満たしていれば、エラーとならないこと。', (field: Field<any>, _) => {

        const maxLength = 10;
        validator.validateMaxLength(field, maxLength);

        expect(field.errors.length).toBe(0);
    });

    test.each([
        [new Field('', '10length...', ''), '11文字丁度'],
        [new Field('', 'this is a string.', ''), '17文字'],
        [new Field('', '11文字の日本語文字だ', ''), '11文字の日本語文字']

    ])('文字列が指定桁数を超過しているとき、fieldのerrorsプロパティにエラーメッセージが格納されること。', (field: Field<any>, _) => {

        const maxLength = 10;
        validator.validateMaxLength(field, maxLength);

        expect(field.errors.length).toBe(1);
        expect(field.errors[0]).toBe(`${field.label}は${maxLength}文字以下で入力してください。`);
    });

});

describe('数値チェック', () => {

    test.each([
        [new Field('', '0', ''), '数値文字列'],
        [new Field('', 123, ''), '普通の数値'],
        [new Field('', 123.456, ''), '実数'],
        [new Field('', -9.1, ''), '負数']

    ])('数値であれば、エラーとならないこと。', (field: Field<any>, _) => {

        validator.validateNum(field);

        expect(field.errors.length).toBe(0);
    });

    test.each([
        [new Field('', 'John Doe', ''), '非数値'],
        [new Field('', '山田太郎', ''), '日本語文字'],
        [new Field('', ' ', ''), '空白']

    ])('数値以外では、エラーメッセージがFieldのerrorsプロパティに格納されること。', (field: Field<any>, _) => {

        validator.validateNum(field);

        expect(field.errors.length).toBe(1);
        expect(field.errors[0]).toBe('数値を入力してください。');
    });

});


describe('半角英数記号チェック', () => {

    test.each([
        [new Field('', 'my_user-Name', ''), '英数と記号'],
        [new Field('', 123, ''), '数値のみ'],
        [new Field('', 'a-pompom', ''), 'ありきたりなユーザ名'],
        [new Field('', '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', ''), '全パターン']

    ])('半角英数と「-_」のみで構成された文字列であれば、エラーとならないこと。', (field: Field<any>, _) => {

        validator.validateAlphaNumericText(field);

        expect(field.errors.length).toBe(0);
    });

    test.each([
        [new Field('', 'John Doe', ''), 'スペースあり'],
        [new Field('', '山田太郎', ''), '日本語文字'],
        [new Field('', '!<>#$%&^', ''), '使用できない記号']

    ])('半角英数と「-_」以外では、エラーメッセージがFieldのerrorsプロパティに格納されること。', (field: Field<any>, _) => {

        validator.validateAlphaNumericText(field);

        expect(field.errors.length).toBe(1);
        expect(field.errors[0]).toBe(`${field.label}は半角英数と_-のみ利用できます。`);
    });

});