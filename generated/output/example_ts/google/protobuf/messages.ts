// Generated by open_horadric. DO NOT EDIT!

import * as interfaces from './interfaces'


export class Empty implements interfaces.IEmpty {

    public constructor (
    ) {
    }

    public static FromData(data: interfaces.IEmptyData): Empty {
        if (data === undefined) {
            return new Empty()
        }

        return new Empty(
        )
    }
}

