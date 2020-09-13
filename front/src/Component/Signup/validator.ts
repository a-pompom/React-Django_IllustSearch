import * as BaseData from 'Common/BaseData';
import { Field } from 'Common/Field';
import { validateMaxLength } from 'Common/Logic/TextValidator';
import * as SignupData from './signupData';

/**
 * ユーザ名を検証 最大長のみを対象とする
 * 
 * @param state 更新対象の状態
 * @param field バリデーション対象のフィールド
 */
export const executeValidate = (
    state: SignupData.State,
    field: Field<SignupData.FieldName, SignupData.Value>,
    value: SignupData.Value
): BaseData.ValidationResult<SignupData.FieldName, SignupData.Value>[] => {

    const results = [];

    // ユーザ名
    if (field.name === 'username') {
        field.value = value;
        field.errors = [];

        const MAX_USERNAME_LENGTH = 255;
        validateMaxLength(field, MAX_USERNAME_LENGTH);

        results.push(field.getValidationResult());
    }

    return results;
};