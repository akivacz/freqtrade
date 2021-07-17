from pandas import DataFrame
from freqtrade.optimize.hyperopt import IHyperOptLoss
from freqtrade.data.btanalysis import calculate_max_drawdown

# higher numbers penalize drawdowns more severely
DRAWDOWN_MULT = 0.4

class ProfitDrawDownHyperOptLoss(IHyperOptLoss):

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int, *args, **kwargs) -> float:
        total_profit = results['profit_abs'].sum()

        # from freqtrade.optimize.optimize_reports.generate_strategy_stats()
        try:
            max_drawdown_per, _, _, _, _ = calculate_max_drawdown(results, value_col='profit_ratio')
        except ValueError:
            max_drawdown_per = 0

        return -1 * (total_profit * (1 - max_drawdown_per * DRAWDOWN_MULT))
