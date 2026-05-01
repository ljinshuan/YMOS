## ADDED Requirements

### Requirement: Compute technical indicators
The system SHALL compute 10 groups of technical indicators on an OHLCV DataFrame using pandas-ta.

#### Scenario: All indicator groups computed
- **WHEN** `compute_indicators` is called with a valid OHLCV DataFrame
- **THEN** the returned DataFrame SHALL contain additional columns for: MA(5/10/20/60/120/250), MACD(12/26/9), ADX(14)/+DI(14)/-DI(14), RSI(6/14), KDJ(9/3/3), Williams %R(14), Bollinger Bands(20,2), ATR(14), OBV, Volume MA(5/20)

#### Scenario: Insufficient data handling
- **WHEN** the input DataFrame has fewer rows than required by an indicator (e.g., less than 250 rows for MA250)
- **THEN** the system SHALL compute all indicators where sufficient data exists and leave columns as NaN where data is insufficient

### Requirement: Multi-timeframe analysis
The system SHALL resample daily data to weekly and monthly timeframes and compute indicators on each.

#### Scenario: Weekly resampling
- **WHEN** `analyze` is called with daily OHLCV data
- **THEN** the system SHALL resample to weekly using `resample('W')` with `open=first, high=max, low=min, close=last, volume=sum` and compute indicators on the weekly DataFrame

#### Scenario: Monthly resampling
- **WHEN** `analyze` is called with daily OHLCV data
- **THEN** the system SHALL resample to monthly using `resample('ME')` with `open=first, high=max, low=min, close=last, volume=sum` and compute indicators on the monthly DataFrame

### Requirement: Signal generation
The system SHALL generate buy/sell/neutral signals for each indicator based on the latest values.

#### Scenario: Signal classification
- **WHEN** `generate_signals` is called with an indicators DataFrame
- **THEN** each indicator SHALL produce a signal of `多头`, `空头`, or `中性` with a human-readable note explaining the signal (e.g., "MACD 金叉", "RSI 超买区 75.2")

#### Scenario: MA signal logic
- **WHEN** the current close price is above MA20 and MA20 > MA60 (bullish alignment)
- **THEN** the MA signal SHALL be `多头` with note describing the alignment

#### Scenario: RSI signal logic
- **WHEN** RSI(14) is above 70
- **THEN** the RSI signal SHALL be `空头` with note "超买"
- **WHEN** RSI(14) is below 30
- **THEN** the RSI signal SHALL be `多头` with note "超卖"

#### Scenario: MACD signal logic
- **WHEN** DIF crosses above DEA
- **THEN** the MACD signal SHALL be `多头` with note "金叉"
- **WHEN** DIF crosses below DEA
- **THEN** the MACD signal SHALL be `空头` with note "死叉"

### Requirement: Summary scoring
The system SHALL produce an overall technical assessment across all three timeframes.

#### Scenario: Summary verdict
- **WHEN** `summarize` is called with daily, weekly, and monthly signals
- **THEN** the system SHALL return a verdict of `偏多 ⬆`, `偏空 ⬇`, or `中性 ➡` based on the ratio of bullish vs bearish signals across all timeframes

#### Scenario: Resonance description
- **WHEN** multiple timeframes show the same direction
- **THEN** the summary SHALL include a resonance note (e.g., "日线/周线共振看多")
