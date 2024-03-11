Consider using Automations and input text fields.

alias: 'Apple TV Activity Monitor to Input Text'
description: 'Monitors activity across all Apple TVs and updates input_text entities.'
trigger:
  - platform: state
    entity_id: media_player.master
    to: 'playing'
  - platform: state
    entity_id: media_player.home_theater
    to: 'playing'
  - platform: state
    entity_id: media_player.living_room_tv
    to: 'on'
condition: []
action:
  - choose:
      - conditions:
          - condition: template
            value_template: "{{ trigger.entity_id == 'media_player.master' }}"
        sequence:
          - service: input_text.set_value
            target:
              entity_id: input_text.master_tv_activity
            data:
              value: >
                {{ trigger.to_state.attributes.media_title | regex_replace(find='[^\\w]', replace=' ') }}
      - conditions:
          - condition: template
            value_template: "{{ trigger.entity_id == 'media_player.home_theater' }}"
        sequence:
          - service: input_text.set_value
            target:
              entity_id: input_text.home_theater_activity
            data:
              value: >
                {{ trigger.to_state.attributes.media_title | regex_replace(find='[^\\w]', replace=' ') }}
      - conditions:
          - condition: template
            value_template: "{{ trigger.entity_id == 'media_player.living_room_tv' }}"
        sequence:
          - service: input_text.set_value
            target:
              entity_id: input_text.living_room_tv_activity
            data:
              value: >
                {% if trigger.to_state.attributes.media_title %}
                  {{ trigger.to_state.attributes.media_title | regex_replace(find='[^\\w]', replace=' ') }}
                {% else %}
                  {{ trigger.to_state.attributes.source | regex_replace(find='[^\\w]', replace=' ') }}
                {% endif %}
mode: restart
