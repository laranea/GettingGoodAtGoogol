import random
from argparse import ArgumentParser
import numpy as np
from trainer import *
from game import Game
from agent import *
from utils import *

if __name__ == '__main__':

    ap = ArgumentParser()
    
    # Agent Parameters
    ap.add_argument("-a", "--agent", type=str, default='q_learn',
                    help="Agent Type")
    ap.add_argument("-al", "--alpha", type=float, default=0.01,
                    help="Alpha")
    ap.add_argument("-ald", "--alpha_decay", type=float, default=1e-5,
                    help="Alpha Decay")
    ap.add_argument("-as", "--alpha_step", type=int, default=1000,
                    help="Alpha Step")
    ap.add_argument("-g", "--gamma", type=float, default=0.9,
                    help="Reward Discount Rate")
    ap.add_argument("-e", "--epsilon", type=float, default=0.1,
                    help="Epsilon")
    ap.add_argument("-ed", "--eps_decay", type=float, default=1e-5,
                    help="Epsilon Decay")
    ap.add_argument("-s", "--s_cost", type=float, default=0,
                    help="Search Cost")
    ap.add_argument("-ql", "--q_learn", type=bool, default=False,
                    help="SARSA")
    ap.add_argument("-qkf", "--q_key_fn", type=str, default="bin",
                    help="Q-Key Fn")
    ap.add_argument("-qkp", "--q_key_params", type=str, default="2_2",
                    help="Q-Key Params")
    ap.add_argument("-vf", "--v_fn", type=str, default="vMax",
                    help="Val Fn")
    
    # Training Game Parameters
    ap.add_argument("-lo", "--lo", type=int, default=1,
                    help="Lo")
    ap.add_argument("-hi", "--hi", type=int, default=100,
                    help="Hi")
    ap.add_argument("-ni", "--n_idx", type=int, default=25,
                    help="N-Idx")
    ap.add_argument("-rp", "--replace", type=bool, default=False,
                    help="Replacement")
    ap.add_argument("-r", "--reward_fn", type=str, default="topN",
                    help="Reward Fn")
    ap.add_argument("-rps", "--reward", type=str, default="5_5_5",
                    help="Reward Params")
    
    # Training Parameters
    ap.add_argument("-ng", "--n_games", type=int, default=1000000,
                    help="N-Games")
    ap.add_argument("-ne", "--n_episodes", type=int, default=1000000,
                    help="N-Episodes")
    ap.add_argument("-np", "--n_print", type=int, default=100000,
                    help="N-Print")
    ap.add_argument("-d", "--delay", type=int, default=0,
                    help="Time Delay")
    ap.add_argument("-cre", "--curr_epoch", type=int, default=100000,
                    help="Curriculum Epoch")     
    ap.add_argument("-crp", "--curr_params", type=str, default="0_0_10_-",
                    help="Curriculum Params")    
    
    # Evaluation Game Parameters
    ap.add_argument("-loe", "--lo_eval", type=int, default=1,
                    help="Lo")
    ap.add_argument("-hie", "--hi_eval", type=int, default=100,
                    help="Hi")
    ap.add_argument("-nie", "--n_idx_eval", type=int, default=25,
                    help="N-Idx")
    ap.add_argument("-rpe", "--replace_eval", type=bool, default=False,
                    help="Replacement")
    ap.add_argument("-re", "--reward_fn_eval", type=str, default="scalar",
                    help="Reward Fn")
    ap.add_argument("-rpse", "--reward_eval", type=str, default="1_1",
                    help="Reward Params Eval")
    
    # Evaluation Parameters
    ap.add_argument("-nge", "--n_games_eval", type=int, default=10000,
                    help="N-Games Eval")
    ap.add_argument("-npe", "--n_print_eval", type=int, default=1000,
                    help="N-Print")
    ap.add_argument("-de", "--delay_eval", type=int, default=0,
                    help="Time Delay")
    
    # Save Path
    ap.add_argument("-fp", "--file_path",
                    help="Save File Path")
    
    args = vars(ap.parse_args())
    
    ##################################################
    # SET UP GAME
    ##################################################
    
    if 'scalar' in args['reward_fn']:
        reward_fn = rewardScalar
        pos, neg = args['reward'].split('_')
        reward = {'pos':int(pos), 'neg':-int(neg)}
        
        c_pos, c_neg, c_op = args['curr_params'].split('_')
        curr_params = {'pos':int(c_pos), 'neg':-int(c_neg), 'op':convertOp(c_op)}
        
    elif 'topN' in args['reward_fn']:
        reward_fn = rewardTopN
        pos, neg, n = args['reward'].split('_')
        reward = {'pos':int(pos), 'neg':-int(neg), 'n':int(n)} 
        
        c_pos, c_neg, c_n, c_op = args['curr_params'].split('_')
        curr_params = {'pos':int(c_pos), 'neg':-int(c_neg), 'n':int(c_n), 'op':convertOp(c_op)}
        
    game_params = {'lo':args['lo'],
                   'hi':args['hi'],
                   'n_idx':args['n_idx'],
                   'replace':args['replace'],
                   'reward_fn':reward_fn,
                   'reward':reward}
    
    game = Game(**game_params)
    
    ##################################################
    # SET UP AGENTS
    ##################################################
    
    if 'bin' in args['q_key_fn']:
        i_bin, v_bin = args['q_key_params'].split('_')
        q_key_fn = qKeyMaxBin
        q_key_params = {'i_bin':int(i_bin), 'v_bin':int(v_bin)}
    elif 'seq' in args['q_key_fn']:
        v_bin = ['q_key_params'].split('_')
        q_key_fn = qKeySeq
        q_key_params = {'v_bin':int(v_bin)}

    if args['v_fn'] == 'vMax':
        v_fn = vMax
        v_key = -1
    if args['v_fn'] == 'vSeq':
        v_fn = vSeq
        v_key = str([0])
    
    ##################################################
    # SET UP Q-LEARNING AGENT
    ##################################################
    
    if args['agent'] == 'q_learn':
    
        agent_params = {'alpha':args['alpha'],
                        'alpha_decay':args['alpha_decay'],
                        'alpha_step':args['alpha_step'],
                      	'gamma':args['gamma'],
                      	'eps':args['epsilon'], 
                      	'eps_decay':args['eps_decay'], 
                      	's_cost':args['s_cost'],
                      	'sarsa':args['q_learn'],
                      	'q_key_fn':q_key_fn,
                        'q_key_params':q_key_params,
                      	'v_fn':v_fn,
                        'v_key':v_key}
        
        agent = QAgent(**agent_params)
        
        trainer_train_params = {'game':game,
                                'agent':agent,
                                'n_games':args['n_games'],
                                'n_print':args['n_print'],
                                'delay':args['delay'],
                                'curriculum':{'epoch':args['curr_epoch'], 'params':curr_params}}
        
        trainer = QTrainer()
    
    ##################################################
    # SET UP MONTE CARLO AGENT
    ##################################################
    
    elif args['agent'] == 'mcmc':
        
        agent_params = {'gamma':args['gamma'],
                      	'eps':args['epsilon'], 
                      	'eps_decay':args['eps_decay'], 
                      	's_cost':args['s_cost'],
                      	'q_key_fn':q_key_fn,
                        'q_key_params':q_key_params,
                      	'v_fn':v_fn,
                        'v_key':v_key}
        
        agent = MCMCAgent(**agent_params)
        
        trainer_train_params = {'game':game,
                                'agent':agent,
                                'n_episodes':args['n_episodes'],
                                'curriculum':{'epoch':args['curr_epoch'], 'params':curr_params}}
        
        trainer = MCMCTrainer()
    
    ##################################################
    # TRAINING
    ##################################################
    
    print('TRAINING')
    trainer.train(**trainer_train_params)
    print('*' * 89)
    print('*' * 89)
    
    ##################################################
    # SET UP EVALUATION
    ##################################################
    
    if 'scalar' in args['reward_fn_eval']:
        reward_fn_eval = rewardScalar
        pos, neg = args['reward_eval'].split('_')
        reward_eval = {'pos':int(pos), 'neg':-int(neg)}
    elif 'topN' in args['reward_fn_eval']:
        reward_fn_eval = rewardTopN
        pos, neg, n = args['reward_eval'].split('_')
        reward_eval = {'pos':int(pos), 'neg':-int(neg), 'n':int(n)} 
        
        
    game_eval_params = {'lo':args['lo_eval'],
                        'hi':args['hi_eval'],
                        'n_idx':args['n_idx_eval'],
                        'replace':args['replace_eval'],
                        'reward_fn':reward_fn_eval,
                        'reward':reward_eval}
    
    game_eval = Game(**game_eval_params)
    
    trainer_eval_params = {'game':game_eval,
                           'agent':agent,
                           'n_games':args['n_games_eval'],
                           'n_print':args['n_print_eval'],
                           'delay':args['delay_eval']}
    
    ##################################################
    # EVALUATION
    ##################################################
    
    print('EVAL')
    trainer.eval(**trainer_eval_params)
    print('*' * 89)
    print('*' * 89)
    
    ##################################################
    # SAVE
    ##################################################
    
    svZipPkl(agent, args['file_path'])
    print("AGENT STORED AT: {}".format(args['file_path']))
