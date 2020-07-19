
/**
 * HTMLの入力エリアを表現する型
 */
export class Field<Value, FieldType=string> {

    // 名称 name属性ではなく、種類を区別するために利用
    private _name: FieldType;
    // 表示名
    private _label: string;
    // 値
    private _value: Value;
    // バリデーションエラー
    private _errors: string[];

    constructor(name: FieldType, value: Value, label: string) {
        this._name = name;
        this._value = value;
        this._label = label;

        this._errors = [];
    }

    // getter/setter---------------------------------------------------------------------------
    get name(): FieldType {
        return this._name;
    }
    set name(newName: FieldType) {
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