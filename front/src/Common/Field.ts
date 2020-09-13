import * as BaseData from './BaseData';

/**
 * HTMLの入力エリアを表現する型
 */
export class Field<FieldName, Value> {

    // 名称 name属性
    private _name: FieldName;
    // 表示名
    private _label: string;
    // 値
    private _value: Value;
    // バリデーションエラー
    private _errors: string[];

    constructor(name: FieldName, value: Value, label: string) {
        this._name = name;
        this._value = value;
        this._label = label;

        this._errors = [];
    }

    /**
     * フィールドに対するバリデーション結果を取得
     * 
     * @returns ValidationResult reducerでStateを更新できるよう、name・値・エラーを個別に保持したresultオブジェクト
     */
    public getValidationResult(): BaseData.ValidationResult<FieldName, Value> {

        const result: BaseData.ValidationResult<FieldName, Value> = {
            isValid: this._errors.length === 0,
            fieldName: this._name,
            fieldValue: this._value,
            errors: this._errors
        }

        return result;
    }

    // getter/setter---------------------------------------------------------------------------
    get name(): FieldName {
        return this._name;
    }
    set name(newName: FieldName) {
        this._name = newName;
    }
    get label(): string {
        return this._label;
    }

    get value(): Value {
        return this._value;
    }
    set value(newValue: Value) {
        this._value = newValue;
    }

    get errors(): string[] {
        return this._errors;
    }
    set errors(newErrors: string[]) {
        this._errors = newErrors;
    }
}