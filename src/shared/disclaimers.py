"""
Shared compliance disclaimers used across multiple domains.

This module provides localized disclaimers that are used by:
- Adelaide domain: Newsletter generation
- Reporters domain: Output formatting

By placing these here, we avoid cross-domain imports
(e.g., Reporters importing from Adelaide).

Principle 1 (DDD): Domains don't directly call each other.
"""

from typing import Dict


# Regional disclaimers by locale
# Used by both Adelaide and Reporters domains
REGIONAL_DISCLAIMERS: Dict[str, str] = {
    'en': """**Important Disclosures**

This content is for educational purposes only and does not constitute investment advice, financial advice, trading advice, or any other sort of advice. diBoaS does not recommend that any cryptocurrency should be bought, sold, or held by you.

Past performance is not indicative of future results. The value of investments can go down as well as up, and you may lose some or all of your investment.

Consider consulting a licensed financial adviser for guidance specific to your situation.

*You decide what's best for your situation.*""",

    'pt-br': """**Avisos Importantes de Conformidade**

**AVISO 1 - PROTEÇÃO AO INVESTIDOR:** Criptoativos NÃO são protegidos por esquemas de garantia de depósitos ou fundos de compensação ao investidor.

**AVISO 2 - RISCO DE PERDA:** O valor dos seus investimentos pode diminuir ou aumentar. Você pode perder parte ou todo o capital investido.

**AVISO 3 - ORIENTAÇÃO PROFISSIONAL:** Considere consultar um assessor financeiro ou profissional habilitado pela CVM para orientação específica à sua situação.

Este conteúdo é apenas para fins educacionais e não constitui aconselhamento de investimento, aconselhamento financeiro, aconselhamento de negociação ou qualquer outro tipo de aconselhamento.

Desempenho passado não é indicativo de resultados futuros.

**Direito de reclamação:** [contato@diboas.com]

*Você decide o que é melhor para sua situação.*""",

    'de': """**Wichtige Compliance-Hinweise**

**HINWEIS 1 - ANLEGERSCHUTZ (MiCA):** Kryptowerte werden NICHT durch EU-Einlagensicherungssysteme oder Anlegerentschädigungsfonds geschützt.

**HINWEIS 2 - VERLUSTRISIKO:** Der Wert Ihrer Anlagen kann steigen oder fallen. Sie können einen Teil oder Ihr gesamtes investiertes Kapital verlieren.

**HINWEIS 3 - PROFESSIONELLE BERATUNG:** Erwägen Sie die Beratung durch einen lizenzierten Finanzberater oder einen von der BaFin zugelassenen Fachmann für Beratung, die auf Ihre spezifische Situation zugeschnitten ist.

Dieser Inhalt dient ausschließlich Bildungszwecken und stellt keine Anlageberatung, Finanzberatung, Handelsberatung oder sonstige Beratung dar.

Die vergangene Wertentwicklung ist kein Indikator für zukünftige Ergebnisse.

*Sie entscheiden, was für Ihre Situation am besten ist.*""",

    'es': """**Avisos Importantes de Cumplimiento**

**AVISO 1 - PROTECCIÓN AL INVERSOR (MiCA):** Los criptoactivos NO están protegidos por sistemas de garantía de depósitos de la UE ni fondos de compensación al inversor.

**AVISO 2 - RIESGO DE PÉRDIDA:** El valor de sus inversiones puede subir o bajar. Usted puede perder parte o todo su capital invertido.

**AVISO 3 - ASESORAMIENTO PROFESIONAL:** Considere consultar con un asesor financiero autorizado o profesional habilitado para orientación específica a su situación.

Este contenido es solo para fines educativos y no constituye asesoramiento de inversión, asesoramiento financiero, asesoramiento de trading o cualquier otro tipo de asesoramiento.

El rendimiento pasado no es indicativo de resultados futuros.

*Usted decide lo que es mejor para su situación.*"""
}


# Hypothetical performance disclaimers (SEC Marketing Rule compliance)
# Used by both Adelaide and Reporters domains
HYPOTHETICAL_DISCLAIMERS: Dict[str, str] = {
    'en': (
        "⚠️ HYPOTHETICAL PERFORMANCE: This analysis is based on historical data "
        "and simulated results. Past performance does not guarantee future returns. "
        "Actual results may differ materially due to market conditions, execution, "
        "and other factors. These results reflect hindsight bias and should not be "
        "relied upon as indicative of future performance."
    ),
    'pt-br': (
        "⚠️ DESEMPENHO HIPOTÉTICO: Esta análise é baseada em dados históricos "
        "e resultados simulados. Desempenho passado não garante retornos futuros. "
        "Resultados reais podem diferir significativamente devido às condições de "
        "mercado, execução e outros fatores. Estes resultados refletem viés de "
        "retrospectiva e não devem ser considerados indicativos de desempenho futuro."
    ),
    'de': (
        "⚠️ HYPOTHETISCHE PERFORMANCE: Diese Analyse basiert auf historischen Daten "
        "und simulierten Ergebnissen. Die vergangene Wertentwicklung garantiert keine "
        "zukünftigen Renditen. Die tatsächlichen Ergebnisse können aufgrund von "
        "Marktbedingungen, Ausführung und anderen Faktoren erheblich abweichen. "
        "Diese Ergebnisse spiegeln Rückschaufehler wider und sollten nicht als "
        "Indikator für zukünftige Performance betrachtet werden."
    ),
    'es': (
        "⚠️ RENDIMIENTO HIPOTÉTICO: Este análisis se basa en datos históricos "
        "y resultados simulados. El rendimiento pasado no garantiza rendimientos futuros. "
        "Los resultados reales pueden diferir materialmente debido a las condiciones del "
        "mercado, la ejecución y otros factores. Estos resultados reflejan sesgo retrospectivo "
        "y no deben considerarse indicativos del rendimiento futuro."
    )
}
