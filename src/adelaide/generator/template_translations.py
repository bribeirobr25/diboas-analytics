"""
Template translation mapping for Adelaide.

Provides all translation keys needed for template rendering.
"""

from typing import Dict
from datetime import datetime


def get_template_translations(localization, locale: str) -> Dict[str, str]:
    """
    Get all template translation keys for the given locale.

    Args:
        localization: LocalizationEngine instance
        locale: Locale code (en, pt-br, de, es)

    Returns:
        Dict of translation key -> translated value
    """
    translate = lambda key: localization.translate(key, locale)

    # Get localized time of day
    hour = datetime.now().hour
    if 5 <= hour < 12:
        time_of_day_localized = translate('good_morning').replace(
            translate('greeting_time_prefix') + ' ', ''
        )
    elif 12 <= hour < 18:
        time_of_day_localized = translate('good_afternoon').replace(
            translate('greeting_time_prefix') + ' ', ''
        )
    else:
        time_of_day_localized = translate('good_evening').replace(
            translate('greeting_time_prefix') + ' ', ''
        )

    return {
        # Page titles and editions
        'page_title': translate('page_title'),
        'rally_edition_label': translate('rally_edition_label'),
        'decline_edition_label': translate('decline_edition_label'),
        'emergency_update_title': translate('emergency_update_title'),
        'crisis_communication_label': translate('crisis_communication_label'),

        # Section titles
        'market_snapshot_title': translate('market_snapshot_title'),
        'good_day_context_title': translate('good_day_context_title'),
        'strategy_performance_title': translate('strategy_performance_title'),
        'what_not_to_do_title': translate('what_not_to_do_title'),
        'insight_section_title': translate('insight_section_title'),
        'whale_watch_title': translate('whale_watch_title'),
        'what_happened_title': translate('what_happened_title'),
        'historical_context_title': translate('historical_context_title'),
        'strategy_impact_title': translate('strategy_impact_title'),
        'your_options_title': translate('your_options_title'),
        'cannot_tell_you_title': translate('cannot_tell_you_title'),
        'adelaide_thought_title': translate('adelaide_thought_title'),
        'consider_speaking_title': translate('consider_speaking_title'),
        'outlook_section_title': translate('outlook_section_title'),

        # Crisis template sections
        'important_update_title': translate('important_update_title'),
        'what_we_know_title': translate('what_we_know_title'),
        'what_investigating_title': translate('what_investigating_title'),
        'what_unknown_title': translate('what_unknown_title'),
        'current_status_title': translate('current_status_title'),
        'acknowledgments_title': translate('acknowledgments_title'),
        'communication_plan_title': translate('communication_plan_title'),
        'transparency_title': translate('transparency_title'),

        # Table labels
        'asset_label': translate('asset'),
        'price_label': translate('price'),
        'change_24h_label': translate('24h_change'),
        'strategy_type_label': translate('strategy_type_label'),
        'today_label': translate('today_label'),
        'todays_impact_label': translate('todays_impact_label'),
        'seven_day_label': translate('seven_day_label'),
        'thirty_day_label': translate('thirty_day_label'),
        'conservative_label': translate('conservative_label'),
        'balanced_label': translate('balanced_label'),
        'growth_label': translate('growth_label'),
        'markets_label': translate('markets_label'),
        'system_status_label': translate('system_status_label'),
        'withdrawals_label': translate('withdrawals_label'),
        'processing_time_label': translate('processing_time_label'),
        'fear_greed_index_label': translate('fear_greed_index'),

        # Whale table
        'whale_table_who': translate('whale_table_who'),
        'whale_table_holding': translate('whale_table_holding'),
        'whale_table_status': translate('whale_table_status'),
        'whale_mtgox_name': translate('whale_mtgox_name'),
        'whale_mtgox_holding': translate('whale_mtgox_holding'),
        'whale_mtgox_status': translate('whale_mtgox_status'),
        'whale_ftx_name': translate('whale_ftx_name'),
        'whale_ftx_holding': translate('whale_ftx_holding'),
        'whale_ftx_status': translate('whale_ftx_status'),
        'whale_ftx_sol_name': translate('whale_ftx_sol_name'),
        'whale_ftx_sol_holding': translate('whale_ftx_sol_holding'),
        'whale_ftx_sol_status': translate('whale_ftx_sol_status'),

        # Greeting
        'greeting_time_prefix': translate('greeting_time_prefix'),
        'time_of_day_localized': time_of_day_localized,

        # Market bullets
        'market_bullets_header': translate('market_bullets_header'),

        # Rally day specific
        'markets_up_intro': translate('markets_up_intro'),
        'good_day_reminder_intro': translate('good_day_reminder_intro'),
        'good_day_point1_bold': translate('good_day_point1_bold'),
        'good_day_point1_text': translate('good_day_point1_text'),
        'good_day_point2_bold': translate('good_day_point2_bold'),
        'good_day_point2_text': translate('good_day_point2_text'),
        'good_day_point3_bold': translate('good_day_point3_bold'),
        'good_day_point3_text': translate('good_day_point3_text'),
        'what_not_to_do_intro': translate('what_not_to_do_intro'),
        'dont_chase_bold': translate('dont_chase_bold'),
        'dont_chase_text': translate('dont_chase_text'),
        'dont_switch_bold': translate('dont_switch_bold'),
        'dont_switch_text': translate('dont_switch_text'),
        'dont_count_bold': translate('dont_count_bold'),
        'dont_count_text': translate('dont_count_text'),
        'plan_discipline_note': translate('plan_discipline_note'),
        'enjoy_green_day_note': translate('enjoy_green_day_note'),
        'whale_disclaimer': translate('whale_disclaimer'),

        # Down day specific
        'lets_talk_today': translate('lets_talk_today'),
        'markets_down_intro': translate('markets_down_intro'),
        'down_days_context': translate('down_days_context'),
        'no_prediction_note': translate('no_prediction_note'),
        'no_wrong_choice': translate('no_wrong_choice'),
        'different_situations_note': translate('different_situations_note'),
        'option1_title': translate('option1_title'),
        'option2_title': translate('option2_title'),
        'option3_title': translate('option3_title'),
        'stay_historical_note': translate('stay_historical_note'),
        'reduce_impact_note': translate('reduce_impact_note'),
        'withdraw_valid_note': translate('withdraw_valid_note'),
        'cannot_tell_1': translate('cannot_tell_1'),
        'cannot_tell_2': translate('cannot_tell_2'),
        'cannot_tell_3': translate('cannot_tell_3'),
        'only_you_know': translate('only_you_know'),
        'consider_adviser_note': translate('consider_adviser_note'),

        # Crisis template specific
        'all_options_valid': translate('all_options_valid'),
        'significant_situation': translate('significant_situation'),
        'crisis_option1_title': translate('crisis_option1_title'),
        'crisis_option1_point1': translate('crisis_option1_point1'),
        'crisis_option1_point2': translate('crisis_option1_point2'),
        'crisis_option2_title': translate('crisis_option2_title'),
        'crisis_option2_point1': translate('crisis_option2_point1'),
        'crisis_option2_point2': translate('crisis_option2_point2'),
        'crisis_option3_title': translate('crisis_option3_title'),
        'cannot_guarantee': translate('cannot_guarantee'),
        'guarantee_text': translate('guarantee_text'),
        'cannot_predict': translate('cannot_predict'),
        'predict_text': translate('predict_text'),
        'cannot_advise': translate('cannot_advise'),
        'advise_text': translate('advise_text'),
        'uncertainty_note': translate('uncertainty_note'),
        'immediate_label': translate('immediate_label'),
        'immediate_text': translate('immediate_text'),
        'next_update_text': translate('next_update_text'),
        'ongoing_label': translate('ongoing_label'),
        'ongoing_text': translate('ongoing_text'),
        'until_stabilizes': translate('until_stabilizes'),
        'support_contact_intro': translate('support_contact_intro'),
        'transparency_statement': translate('transparency_statement'),
        'reviewed_approved': translate('reviewed_approved'),

        # Common
        'you_decide': translate('you_decide'),
    }
