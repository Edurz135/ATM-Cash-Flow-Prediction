# Predicción de la Demanda de Retiros Diarios en ATMs

## Conjunto de Datos Inicial

- **ATM Name**: Nombre del ATM
- **Transaction Date**: Fecha de la transacción
- **No. of Withdrawals**: Número de retiros
- **No. of XYZ Card Withdrawals**: Número de retiros con tarjeta XYZ
- **No. of Other Card Withdrawals**: Número de retiros con otras tarjetas
- **Total Amount Withdrawn**: Monto total retirado
- **Amount Withdrawn XYZ Card**: Monto retirado con tarjeta XYZ
- **Amount Withdrawn Other Card**: Monto retirado con otras tarjetas

## Feature Engineering

- **Type**: Tipo de día (feriado nacional, estación del año, observancia, ...)
- **Weekday**: Día de la semana (MONDAY, TUESDAY, ...)

### Secuencia de Días Festivos
- **Holiday Sequence**: Secuencia de días feriados y laborables (ej. WWW, WHW, HHH)
- **isYesterdayHoliday**: ¿Ayer fue feriado? (True/False)
- **isHoliday**: ¿Es feriado hoy? (True/False)
- **isTomorrowHoliday**: ¿Mañana es feriado? (True/False)

### Secuencia de Días Laborables
- **isYesterdayWeekday**: ¿Ayer fue día laborable? Lunes a viernes (True/False)
- **isWeekday**: ¿Es día laborable hoy? Lunes a viernes (True/False)
- **isTomorrowWeekday**: ¿Mañana es día laborable? Lunes a viernes (True/False)

### Períodos de Pago
> Se usa los criterios de feriado y día de trabajo.
- **isPaymentDay**: ¿Es día de pago (fin de mes o quincena)? (True/False)
- **isPayweek**: ¿Es la semana de pago (quincena o fin de mes)? (True/False)

### Más métricas
- **rolling_mean_weekday**: The average demand for two days of the same past (on two Tuesdays, on two Wednesdays) (True/False)
- **rolling_max**: Maximum demand value for the week
- **lag_6**: The amount of demand seix days ago
- **rolling_max_weekday**: The maximum demand value for two of the same past days of the week (on two Tuesdays, on two Wednesdays)
- **rolling_std**: Weekly demand standard deviation
- **rolling_mean**: Average monthly demand value