import * as LoginData from 'Component/Login/loginData';
import { Phase } from 'Common/Phase';
import { Field } from 'Common/Field';

export const users = [
    { username: '背景', iconPath: 'static/icon.png'},
    { username: '写真用', iconPath: 'static/写真.jpg'},
    { username: 'root', iconPath: 'resources/root.png'},
];

export const getInitialState = (): LoginData.State => ({
    phase: new Phase('IDLE'),
    username: new Field('username', '', 'ユーザ名'),
    users: []
});