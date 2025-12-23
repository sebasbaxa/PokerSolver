import api from './client';

export interface SolveRequest {
    oop_range: string[];
    ip_range: string[];
    oop_stack: number;
    ip_stack: number;
    oop_contribution: number;
    ip_contribution: number;
    pot: number;
    flop: string[];
}

export interface HandStrategy {
    hand: string;
    fold: number;
    call: number;
    raise: number;
    ev: number;
}

export interface SolveResponse {
    message: string;
    oop_strategy: HandStrategy[];
    ip_strategy: HandStrategy[];
}

export const solverApi = {
    solve: async (request: SolveRequest) => {
        const response = await api.post<SolveResponse>('/solver/solve', request);
        return response.data;                                                       
    }
}