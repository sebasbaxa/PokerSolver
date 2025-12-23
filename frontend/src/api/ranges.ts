import api from './client';


export interface RangeResponse {
    player: string;
    hands: string[];
    count: number
}

export const rangesApi = {
    createRange: async (player: string, hands: string[]) => {
        const response = await api.post<RangeResponse>('/ranges/create', {
            player,
            hands
        });
        return response.data;
    },
    getPresets: async () => {
        const response = await api.get<Record<string, string[]>>('/ranges/presets');
        return response.data;
    }
}