import { User, UserResponse } from './loginData';
import { FetchUtil } from 'Common/FetchUtil';

const END_POINT = 'http://localhost:8000/api/v1';

/**
 * APIよりカテゴリの一覧を取得
 */
export const getUserList = async (): Promise<User[]> => {

    const response = await FetchUtil.get<UserResponse>(`${END_POINT}/login`);
    console.log(response);

    // レスポンス→View用オブジェクトへ詰め替え
    const userList = response.users.map((user) => {

        return {
            username: user.username,
            iconPath: ''
        };
    });

    return userList;
};