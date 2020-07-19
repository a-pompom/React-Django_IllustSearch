import { Field } from './Field';

/**
 * 最小桁数に満たないか。
 * 
 * @param field 検査対象フィールド
 * @param minLength 最小桁数
 */
export const validateMinLength = <Value>(field: Field<Value>, minLength: number): void => {
    
    const target = String(field.value).length;

    const ERROR_MESSAGE = `${field.label}は${minLength}文字以上で入力してください。`;

    if (target < minLength) {
        field.errors.push(ERROR_MESSAGE);
    }

    return;
};
/**
 * 最大桁数を超過しているか。
 * 
 * @param field 検査対象フィールド
 * @param maxLength 最大桁数
 */
export const validateMaxLength = <Value>(field: Field<Value>, maxLength: number): void => {
    
    const target = String(field.value).length;

    const ERROR_MESSAGE = `${field.label}は${maxLength}文字以下で入力してください。`;

    if (target > maxLength) {
        field.errors.push(ERROR_MESSAGE);
    }

    return;
};

/**
 * 入力値が数値か検証。
 * 
 * @param field 検証対象の入力フィールド
 */
export const validateNum = <Value>(field: Field<Value>): void => {

    const isNumeric = /^[-]?([1-9]\d*|0)(\.\d+)?$/.test(String(field.value));

    const ERROR_MESSAGE = '数値を入力してください。';

    if (!isNumeric) {
        field.errors.push(ERROR_MESSAGE);
    }

    return;
};

/**
 * 入力値が半角英数と-_のみで構成されているか検証
 * 
 * @param field バリデーション対象
 */
export const validateAlphaNumericText = <Value>(field: Field<Value>): void => {

    const target = String(field.value);

    const ERROR_MESSAGE = `${field.label}は半角英数と_-のみ利用できます。`;

    if (!/^[0-9A-Za-z\-\_]+$/.test(target)) {
        field.errors.push(ERROR_MESSAGE);
    }

    return;
}