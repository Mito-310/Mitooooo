import streamlit as st
import random

# 英検2級頻出単語リスト（例）
words = [
    'admit', 'adventure', 'afford', 'appreciate', 'medicine', 'population', 'rely', 'conversation',
    'exactly', 'spirit', 'treat', 'anxious', 'unless', 'frankly', 'whisper', 'appointment',
    'decoration', 'decrease', 'despite', 'explanation', 'explorer', 'furniture', 'further',
    'charity', 'spare', 'forecast', 'audience', 'impress', 'apply', 'instruction', 'award',
    'destroy', 'generally', 'contain', 'sweep', 'ideal', 'chew', 'modern', 'author', 'nation',
    'ceremony', 'direction', 'issue', 'silly', 'eventually', 'ancestor', 'memorize', 'corporation',
    'product', 'citizen', 'prove', 'commercial', 'disappoint', 'journey', 'originally', 'soil',
    'fantastic', 'attractive', 'prevent', 'examination', 'role', 'courage', 'silence', 'confident',
    'emotion', 'nod', 'recommend', 'surround', 'hire', 'chemistry', 'require', 'forgive', 'stare',
    'exhibit', 'suggestion', 'constant', 'exhibition', 'operation', 'receipt', 'survive', 'otherwise',
    'suitable', 'avenue', 'earn', 'enemy', 'achieve', 'advertisement', 'instrument', 'organize',
    'unfortunately', 'describe', 'employ', 'examine', 'harmful', 'importance', 'region', 'relation',
    'rough', 'remind', 'surface'
]

# 簡易英単語辞書(正解とする短い単語の例)
# ※実際はもっと多くの単語を用意するのが望ましいです
dictionary = set([
    'ad', 'it', 'admit', 'venture', 'afford', 'appreciate', 'med', 'medicine', 'pop', 'population',
    'rely', 'con', 'conversation', 'exact', 'exactly', 'spirit', 'treat', 'anxious', 'unless',
    'frank', 'frankly', 'whisper', 'appointment', 'decoration', 'decrease', 'despite',
    'explain', 'explanation', 'explore', 'explorer', 'furnish', 'furniture', 'further',
    'charity', 'spare', 'forecast', 'audience', 'impress', 'apply', 'instruct', 'instruction',
    'award', 'destroy', 'generally', 'contain', 'sweep', 'ideal', 'chew', 'modern', 'author',
    'nation', 'ceremony', 'direction', 'issue', 'silly', 'event', 'eventually', 'ancestor',
    'memorize', 'corporation', 'product', 'citizen', 'prove', 'commercial', 'disappoint',
    'journey', 'original', 'originally', 'soil', 'fantastic', 'attractive', 'prevent',
    'examination', 'role', 'courage', 'silence', 'confident', 'emotion', 'nod', 'recommend',
    'surround', 'hire', 'chemistry', 'require', 'forgive', 'stare', 'exhibit', 'suggestion',
    'constant', 'exhibition', 'operation', 'receipt', 'survive', 'otherwise', 'suitable',
    'avenue', 'earn', 'enemy', 'achieve', 'advertisement'
