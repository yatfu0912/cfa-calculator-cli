"""Interactive mode for CFA Calculator."""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, FloatPrompt, IntPrompt
from rich.table import Table
from rich import box
from typing import Optional, List
import sys

console = Console()


class InteractiveMode:
    """Interactive CLI interface for CFA Calculator."""

    def __init__(self):
        self.running = True

    def run(self):
        """Start the interactive mode."""
        self.show_welcome()

        while self.running:
            try:
                self.show_main_menu()
                choice = Prompt.ask(
                    "\n[bold cyan]選擇模塊 / Select Module[/bold cyan]",
                    choices=["1", "2", "3", "4", "5", "6", "q"],
                    default="q"
                )

                if choice == "q":
                    self.exit_interactive()
                    break
                elif choice == "1":
                    self.tvm_menu()
                elif choice == "2":
                    self.portfolio_menu()
                elif choice == "3":
                    self.bond_menu()
                elif choice == "4":
                    self.stats_menu()
                elif choice == "5":
                    self.other_menu()
                elif choice == "6":
                    self.show_help()

            except KeyboardInterrupt:
                console.print("\n\n[yellow]按 Ctrl+C 退出 / Press Ctrl+C to exit[/yellow]")
                if Confirm.ask("確定退出？ / Exit?", default=False):
                    self.exit_interactive()
                    break
            except Exception as e:
                console.print(f"\n[red]錯誤 / Error: {str(e)}[/red]")
                Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def show_welcome(self):
        """Display welcome message."""
        welcome_text = """
[bold cyan]CFA Calculator - 交互式模式 / Interactive Mode[/bold cyan]

歡迎使用 CFA 計算器！
Welcome to CFA Calculator!

在這個模式下，您可以逐步輸入參數進行計算。
In this mode, you can input parameters step-by-step.
        """
        console.print(Panel(welcome_text, border_style="cyan", box=box.DOUBLE))

    def show_main_menu(self):
        """Display main menu."""
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("選項 / Option", style="cyan", width=12)
        table.add_column("模塊 / Module", style="green")
        table.add_column("說明 / Description", style="yellow")

        table.add_row("1", "TVM", "時間價值 / Time Value of Money")
        table.add_row("2", "Portfolio", "投資組合 / Portfolio Management")
        table.add_row("3", "Bond", "債券 / Fixed Income")
        table.add_row("4", "Stats", "統計 / Statistics")
        table.add_row("5", "Other", "其他計算 / Other Calculations")
        table.add_row("6", "Help", "幫助 / Help")
        table.add_row("q", "Quit", "退出 / Exit")

        console.print("\n")
        console.print(table)

    def tvm_menu(self):
        """Time Value of Money submenu."""
        console.print("\n[bold cyan]═══ 時間價值計算 / Time Value of Money ═══[/bold cyan]\n")

        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("選項 / Option", style="cyan", width=12)
        table.add_column("計算 / Calculation", style="green")

        table.add_row("1", "未來值 / Future Value (FV)")
        table.add_row("2", "現值 / Present Value (PV)")
        table.add_row("3", "年金 / Annuity")
        table.add_row("4", "永續年金 / Perpetuity")
        table.add_row("5", "實際年利率 / Effective Annual Rate (EAR)")
        table.add_row("b", "返回 / Back")

        console.print(table)

        choice = Prompt.ask(
            "\n選擇計算 / Select calculation",
            choices=["1", "2", "3", "4", "5", "b"],
            default="b"
        )

        if choice == "b":
            return
        elif choice == "1":
            self.calculate_fv()
        elif choice == "2":
            self.calculate_pv()
        elif choice == "3":
            self.calculate_annuity()
        elif choice == "4":
            self.calculate_perpetuity()
        elif choice == "5":
            self.calculate_ear()

    def calculate_fv(self):
        """Calculate Future Value interactively."""
        from cfa_calculator.formulas.tvm_formulas import calculate_fv
        from cfa_calculator.utils.formatters import format_result

        console.print("\n[bold green]計算未來值 / Calculate Future Value[/bold green]\n")

        pv = FloatPrompt.ask("現值 / Present Value (PV)")
        rate = FloatPrompt.ask("年利率 / Annual Rate (例如 0.05 代表 5%)")
        n = IntPrompt.ask("年數 / Number of Years")
        freq = IntPrompt.ask("複利頻率 / Compounding Frequency (1=年, 2=半年, 4=季, 12=月)", default=1)

        result = calculate_fv(pv, rate, n, freq)

        inputs = {
            "現值 / Present Value (PV)": pv,
            "利率 / Interest Rate": f"{rate * 100:.2f}%",
            "年數 / Years": n,
            "複利頻率 / Frequency": freq,
        }

        results = {"未來值 / Future Value (FV)": result}

        format_result("未來值計算 / Future Value Calculation", inputs, results, "FV = PV × (1 + r/freq)^(n×freq)")

        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def calculate_pv(self):
        """Calculate Present Value interactively."""
        from cfa_calculator.formulas.tvm_formulas import calculate_pv
        from cfa_calculator.utils.formatters import format_result

        console.print("\n[bold green]計算現值 / Calculate Present Value[/bold green]\n")

        fv = FloatPrompt.ask("未來值 / Future Value (FV)")
        rate = FloatPrompt.ask("年利率 / Annual Rate (例如 0.05 代表 5%)")
        n = IntPrompt.ask("年數 / Number of Years")
        freq = IntPrompt.ask("複利頻率 / Compounding Frequency (1=年, 2=半年, 4=季, 12=月)", default=1)

        result = calculate_pv(fv, rate, n, freq)

        inputs = {
            "未來值 / Future Value (FV)": fv,
            "利率 / Interest Rate": f"{rate * 100:.2f}%",
            "年數 / Years": n,
            "複利頻率 / Frequency": freq,
        }

        results = {"現值 / Present Value (PV)": result}

        format_result("現值計算 / Present Value Calculation", inputs, results, "PV = FV / (1 + r/freq)^(n×freq)")

        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def calculate_annuity(self):
        """Calculate Annuity interactively."""
        from cfa_calculator.formulas.tvm_formulas import calculate_annuity_fv, calculate_annuity_pv
        from cfa_calculator.utils.formatters import format_result

        console.print("\n[bold green]計算年金 / Calculate Annuity[/bold green]\n")

        calc_type = Prompt.ask(
            "計算類型 / Calculation Type",
            choices=["fv", "pv"],
            default="pv"
        )

        pmt = FloatPrompt.ask("每期支付 / Payment per Period (PMT)")
        rate = FloatPrompt.ask("每期利率 / Rate per Period (例如 0.05 代表 5%)")
        n = IntPrompt.ask("期數 / Number of Periods")

        annuity_type = Prompt.ask(
            "年金類型 / Annuity Type",
            choices=["ordinary", "due"],
            default="ordinary"
        )

        if calc_type == "fv":
            result = calculate_annuity_fv(pmt, rate, n, annuity_type)
            result_label = "未來值 / Future Value (FV)"
            title = "年金未來值 / Annuity Future Value"
        else:
            result = calculate_annuity_pv(pmt, rate, n, annuity_type)
            result_label = "現值 / Present Value (PV)"
            title = "年金現值 / Annuity Present Value"

        inputs = {
            "支付 / Payment (PMT)": pmt,
            "利率 / Rate": f"{rate * 100:.2f}%",
            "期數 / Periods": n,
            "類型 / Type": annuity_type,
        }

        results = {result_label: result}

        format_result(title, inputs, results)

        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def calculate_perpetuity(self):
        """Calculate Perpetuity interactively."""
        from cfa_calculator.formulas.tvm_formulas import calculate_perpetuity, calculate_growing_perpetuity
        from cfa_calculator.utils.formatters import format_result

        console.print("\n[bold green]計算永續年金 / Calculate Perpetuity[/bold green]\n")

        pmt = FloatPrompt.ask("每期支付 / Payment per Period (PMT)")
        rate = FloatPrompt.ask("利率 / Rate (例如 0.05 代表 5%)")

        has_growth = Confirm.ask("是否有增長率？ / Has growth rate?", default=False)

        if has_growth:
            growth_rate = FloatPrompt.ask("增長率 / Growth Rate (例如 0.03 代表 3%)")
            result = calculate_growing_perpetuity(pmt, rate, growth_rate)
            title = "增長永續年金 / Growing Perpetuity"
            inputs = {
                "支付 / Payment (PMT)": pmt,
                "折現率 / Discount Rate": f"{rate * 100:.2f}%",
                "增長率 / Growth Rate": f"{growth_rate * 100:.2f}%",
            }
        else:
            result = calculate_perpetuity(pmt, rate)
            title = "永續年金 / Perpetuity"
            inputs = {
                "支付 / Payment (PMT)": pmt,
                "利率 / Rate": f"{rate * 100:.2f}%",
            }

        results = {"現值 / Present Value (PV)": result}

        format_result(title, inputs, results)

        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def calculate_ear(self):
        """Calculate Effective Annual Rate interactively."""
        from cfa_calculator.formulas.tvm_formulas import calculate_ear
        from cfa_calculator.utils.formatters import format_result

        console.print("\n[bold green]計算實際年利率 / Calculate Effective Annual Rate[/bold green]\n")

        stated_rate = FloatPrompt.ask("名義年利率 / Stated Annual Rate (例如 0.08 代表 8%)")
        freq = IntPrompt.ask("複利頻率 / Compounding Frequency (1=年, 2=半年, 4=季, 12=月)")

        result = calculate_ear(stated_rate, freq)

        inputs = {
            "名義利率 / Stated Rate": f"{stated_rate * 100:.2f}%",
            "複利頻率 / Frequency": freq,
        }

        results = {"實際年利率 / EAR": f"{result * 100:.4f}%"}

        format_result("實際年利率 / Effective Annual Rate", inputs, results, "EAR = (1 + stated_rate/freq)^freq - 1")

        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def portfolio_menu(self):
        """Portfolio Management submenu."""
        console.print("\n[bold cyan]═══ 投資組合管理 / Portfolio Management ═══[/bold cyan]\n")

        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("選項 / Option", style="cyan", width=12)
        table.add_column("計算 / Calculation", style="green")

        table.add_row("1", "夏普比率 / Sharpe Ratio")
        table.add_row("2", "特雷諾比率 / Treynor Ratio")
        table.add_row("3", "詹森阿爾法 / Jensen's Alpha")
        table.add_row("4", "貝塔 / Beta")
        table.add_row("5", "CAPM")
        table.add_row("b", "返回 / Back")

        console.print(table)

        choice = Prompt.ask(
            "\n選擇計算 / Select calculation",
            choices=["1", "2", "3", "4", "5", "b"],
            default="b"
        )

        if choice == "b":
            return
        elif choice == "1":
            self.calculate_sharpe()
        elif choice == "2":
            self.calculate_treynor()
        elif choice == "3":
            self.calculate_alpha()
        elif choice == "4":
            self.calculate_beta()
        elif choice == "5":
            self.calculate_capm()

    def calculate_sharpe(self):
        """Calculate Sharpe Ratio interactively."""
        from cfa_calculator.formulas.portfolio_formulas import calculate_sharpe_ratio
        from cfa_calculator.utils.formatters import format_result

        console.print("\n[bold green]計算夏普比率 / Calculate Sharpe Ratio[/bold green]\n")

        portfolio_return = FloatPrompt.ask("投資組合回報 / Portfolio Return (例如 0.12 代表 12%)")
        risk_free_rate = FloatPrompt.ask("無風險利率 / Risk-Free Rate (例如 0.03 代表 3%)")
        portfolio_std = FloatPrompt.ask("投資組合標準差 / Portfolio Std Dev (例如 0.15 代表 15%)")

        result = calculate_sharpe_ratio(portfolio_return, risk_free_rate, portfolio_std)

        inputs = {
            "投資組合回報 / Portfolio Return": f"{portfolio_return * 100:.2f}%",
            "無風險利率 / Risk-Free Rate": f"{risk_free_rate * 100:.2f}%",
            "標準差 / Std Dev": f"{portfolio_std * 100:.2f}%",
        }

        results = {"夏普比率 / Sharpe Ratio": f"{result:.4f}"}

        format_result(
            "夏普比率 / Sharpe Ratio",
            inputs,
            results,
            "Sharpe = (Rp - Rf) / σp",
            "數值越高表示風險調整後回報越好 / Higher value indicates better risk-adjusted return"
        )

        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def calculate_treynor(self):
        """Calculate Treynor Ratio interactively."""
        from cfa_calculator.formulas.portfolio_formulas import calculate_treynor_ratio
        from cfa_calculator.utils.formatters import format_result

        console.print("\n[bold green]計算特雷諾比率 / Calculate Treynor Ratio[/bold green]\n")

        portfolio_return = FloatPrompt.ask("投資組合回報 / Portfolio Return (例如 0.15 代表 15%)")
        risk_free_rate = FloatPrompt.ask("無風險利率 / Risk-Free Rate (例如 0.03 代表 3%)")
        beta = FloatPrompt.ask("貝塔 / Beta")

        result = calculate_treynor_ratio(portfolio_return, risk_free_rate, beta)

        inputs = {
            "投資組合回報 / Portfolio Return": f"{portfolio_return * 100:.2f}%",
            "無風險利率 / Risk-Free Rate": f"{risk_free_rate * 100:.2f}%",
            "貝塔 / Beta": f"{beta:.4f}",
        }

        results = {"特雷諾比率 / Treynor Ratio": f"{result:.4f}"}

        format_result("特雷諾比率 / Treynor Ratio", inputs, results, "Treynor = (Rp - Rf) / βp")

        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def calculate_alpha(self):
        """Calculate Jensen's Alpha interactively."""
        from cfa_calculator.formulas.portfolio_formulas import calculate_jensens_alpha
        from cfa_calculator.utils.formatters import format_result

        console.print("\n[bold green]計算詹森阿爾法 / Calculate Jensen's Alpha[/bold green]\n")

        portfolio_return = FloatPrompt.ask("投資組合回報 / Portfolio Return (例如 0.15 代表 15%)")
        risk_free_rate = FloatPrompt.ask("無風險利率 / Risk-Free Rate (例如 0.03 代表 3%)")
        beta = FloatPrompt.ask("貝塔 / Beta")
        market_return = FloatPrompt.ask("市場回報 / Market Return (例如 0.11 代表 11%)")

        result = calculate_jensens_alpha(portfolio_return, risk_free_rate, beta, market_return)

        inputs = {
            "投資組合回報 / Portfolio Return": f"{portfolio_return * 100:.2f}%",
            "無風險利率 / Risk-Free Rate": f"{risk_free_rate * 100:.2f}%",
            "貝塔 / Beta": f"{beta:.4f}",
            "市場回報 / Market Return": f"{market_return * 100:.2f}%",
        }

        results = {"詹森阿爾法 / Jensen's Alpha": f"{result * 100:.4f}%"}

        format_result(
            "詹森阿爾法 / Jensen's Alpha",
            inputs,
            results,
            "α = Rp - [Rf + βp(Rm - Rf)]",
            "正值表示超額表現 / Positive value indicates outperformance"
        )

        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def calculate_beta(self):
        """Calculate Beta interactively."""
        from cfa_calculator.formulas.portfolio_formulas import calculate_beta
        from cfa_calculator.utils.formatters import format_result

        console.print("\n[bold green]計算貝塔 / Calculate Beta[/bold green]\n")
        console.print("[yellow]請輸入歷史回報數據（用逗號分隔）[/yellow]")
        console.print("[yellow]Please enter historical returns (comma-separated)[/yellow]\n")

        asset_returns_str = Prompt.ask("資產回報 / Asset Returns (例如: 0.10,0.15,0.12,0.08)")
        market_returns_str = Prompt.ask("市場回報 / Market Returns (例如: 0.08,0.12,0.10,0.06)")

        asset_returns = [float(x.strip()) for x in asset_returns_str.split(",")]
        market_returns = [float(x.strip()) for x in market_returns_str.split(",")]

        result = calculate_beta(asset_returns, market_returns)

        inputs = {
            "資產回報數據點 / Asset Returns": len(asset_returns),
            "市場回報數據點 / Market Returns": len(market_returns),
        }

        results = {"貝塔 / Beta": f"{result:.4f}"}

        format_result(
            "貝塔計算 / Beta Calculation",
            inputs,
            results,
            "β = Cov(Ra, Rm) / Var(Rm)",
            "β > 1: 比市場波動大 / More volatile than market\nβ < 1: 比市場波動小 / Less volatile\nβ = 1: 與市場相同 / Same as market"
        )

        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def calculate_capm(self):
        """Calculate CAPM interactively."""
        from cfa_calculator.formulas.portfolio_formulas import calculate_capm
        from cfa_calculator.utils.formatters import format_result

        console.print("\n[bold green]計算 CAPM 要求回報 / Calculate CAPM Required Return[/bold green]\n")

        risk_free_rate = FloatPrompt.ask("無風險利率 / Risk-Free Rate (例如 0.03 代表 3%)")
        beta = FloatPrompt.ask("貝塔 / Beta")
        market_return = FloatPrompt.ask("市場回報 / Market Return (例如 0.11 代表 11%)")

        result = calculate_capm(risk_free_rate, beta, market_return)

        inputs = {
            "無風險利率 / Risk-Free Rate": f"{risk_free_rate * 100:.2f}%",
            "貝塔 / Beta": f"{beta:.4f}",
            "市場回報 / Market Return": f"{market_return * 100:.2f}%",
        }

        results = {"要求回報 / Required Return": f"{result * 100:.4f}%"}

        format_result("CAPM 要求回報 / CAPM Required Return", inputs, results, "E(Ri) = Rf + βi[E(Rm) - Rf]")

        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def bond_menu(self):
        """Fixed Income submenu - placeholder."""
        console.print("\n[yellow]債券計算模塊開發中... / Bond module under development...[/yellow]")
        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def stats_menu(self):
        """Statistics submenu - placeholder."""
        console.print("\n[yellow]統計模塊開發中... / Statistics module under development...[/yellow]")
        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def other_menu(self):
        """Other calculations submenu - placeholder."""
        console.print("\n[yellow]其他計算模塊開發中... / Other calculations module under development...[/yellow]")
        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def show_help(self):
        """Show help information."""
        help_text = """
[bold cyan]CFA Calculator 幫助 / Help[/bold cyan]

[bold]交互式模式 / Interactive Mode:[/bold]
- 選擇模塊和計算類型
- 逐步輸入參數
- 查看格式化的結果

[bold]命令行模式 / Command Line Mode:[/bold]
您也可以直接使用命令行：
You can also use command line directly:

  cfa tvm fv --pv 1000 --rate 0.05 --n 10
  cfa portfolio sharpe --return 0.12 --rf 0.03 --std 0.15

[bold]獲取更多幫助 / Get More Help:[/bold]
  cfa --help
  cfa tvm --help
  cfa portfolio --help

[bold]GitHub:[/bold]
  https://github.com/yatfu0912/cfa-calculator-cli
        """
        console.print(Panel(help_text, border_style="cyan"))
        Prompt.ask("\n按 Enter 繼續 / Press Enter to continue")

    def exit_interactive(self):
        """Exit interactive mode."""
        console.print("\n[bold green]感謝使用 CFA Calculator！[/bold green]")
        console.print("[bold green]Thank you for using CFA Calculator![/bold green]\n")
        self.running = False


def start_interactive():
    """Start the interactive mode."""
    interactive = InteractiveMode()
    interactive.run()
