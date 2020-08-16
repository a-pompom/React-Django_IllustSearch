import * as BaseData from 'Common/BaseData';
import { Field } from 'Common/Field';
import * as SignupData from './signupData';

/**
 * 各フィールド値の妥当性を検証
 * 
 * @param state 更新対象の状態
 * @param field バリデーション対象のフィールド
 */
export const executeValidate = (
    state: SignupData.State,
    field: Field<SignupData.Value, SignupData.FieldName>,
    value: SignupData.Value
): BaseData.ValidationResult<SignupData.Value, SignupData.FieldName>[] => {

    const results = [];

    // ユーザ名 [文字種別チェック]
    if (field.name === 'username') {
        field.value = value;

        field.errors = [];

        results.push(field.getValidationResult());
    }

    return results;
};