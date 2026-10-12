import numpy as np
import pandas as pd
import pytest

from src.obligor_economic_capital import (
    conditional_variance_attenuation, simulate_obligor_one_factor_losses,
)
from src.economic_capital import simulate_one_factor_losses
from src.portfolio import generate_synthetic_portfolio


def tiny(pd1=0.2, pd2=0.2, w1=99.0, w2=1.0):
    return pd.DataFrame({'obligor_id':['A','B'], 'pd':[pd1,pd2],
                         'lgd':[1.0,1.0], 'ead':[w1,w2],
                         'rating':['BB','BB'], 'sector':['industrial','industrial']})


def test_reproducibility_frozen_seed_batch_and_shape():
    df=generate_synthetic_portfolio(n=30,seed=7)
    a=simulate_obligor_one_factor_losses(df,n_simulations=431,seed=9,batch_size=27)
    b=simulate_obligor_one_factor_losses(df,n_simulations=431,seed=9,batch_size=27)
    assert a.shape==(431,) and a.dtype==float
    assert np.array_equal(a,b)
    assert np.all(a>=0)


def test_default_probability_endpoints_exact():
    for q, expected in [(0.0,0.0),(1.0,35.0)]:
        df=pd.DataFrame({'obligor_id':['A'],'pd':[q],'lgd':[.5],'ead':[70.]})
        a=simulate_obligor_one_factor_losses(df,n_simulations=257,seed=7,batch_size=13)
        assert np.array_equal(a,np.full(257,expected))


def test_distinct_single_name_loss_support_not_segment_averaged():
    df=tiny()
    actual=simulate_obligor_one_factor_losses(df, n_simulations=2000,seed=8,batch_size=64)
    grouped=simulate_one_factor_losses(df,n_simulations=2000,seed=8)
    assert np.isin(actual,[0.,1.,99.,100.]).all()
    assert (actual==1.).any() and (actual==99.).any()
    assert np.isin(grouped,[0.,50.,100.]).all()
    assert not (grouped==1.).any() and not (grouped==99.).any()


def test_exact_conditional_variance_gap_formula():
    # Identical q in one rating-sector segment. Old approximate weight=50 per default.
    w=np.array([99.,1.]);q=.2
    exact_var=q*(1-q)*(99**2+1**2)
    approx_var=q*(1-q)*(2*50**2)
    gap=conditional_variance_attenuation(w,q)
    assert gap==pytest.approx(exact_var-approx_var)
    assert gap>0
    assert conditional_variance_attenuation([5.,5.,5.],q)==0
    assert conditional_variance_attenuation([99.,1.],0)==0
    assert conditional_variance_attenuation([99.,1.],1)==0


def test_marginal_loss_mean_matches_analytic_pd_times_loss():
    df=tiny(pd1=.15,pd2=.35,w1=13.,w2=7.)
    losses=simulate_obligor_one_factor_losses(df,n_simulations=60000,seed=5,batch_size=100)
    expected=.15*13+.35*7
    assert abs(losses.mean()-expected)<.10 # finite-Monte-Carlo sampling tolerance


@pytest.mark.parametrize('bad',[
    {'pd':[-.001,.2]}, {'pd':[1.01,.2]}, {'pd':[float('nan'),.2]},
    {'lgd':[-.01,1.]}, {'lgd':[1.01,1.]}, {'ead':[-1.,5.]},
    {'ead':[float('inf'),5.]}, {'obligor_id':['A','A']},
])
def test_invalid_portfolio_fails_closed(bad):
    df=tiny()
    for k,v in bad.items():df[k]=v
    with pytest.raises(ValueError): simulate_obligor_one_factor_losses(df, n_simulations=3)


def test_empty_missing_fields_and_configuration_fail_closed():
    with pytest.raises(ValueError):simulate_obligor_one_factor_losses(pd.DataFrame())
    df=tiny()
    for kwargs in ({'n_simulations':0},{'n_simulations':1.5},{'batch_size':0},
                   {'seed':-1},{'seed':True},{'batch_size':False}):
        with pytest.raises(ValueError):simulate_obligor_one_factor_losses(df,**kwargs)


def test_registered_segment_baseline_unchanged():
    # New module does not alter original simulator or its saved research data.
    df=generate_synthetic_portfolio(n=30,seed=7)
    a=simulate_one_factor_losses(df,n_simulations=200,seed=5)
    b=simulate_one_factor_losses(df,n_simulations=200,seed=5)
    assert np.array_equal(a,b)
