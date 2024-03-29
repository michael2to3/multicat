from abc import ABC, abstractmethod


class HashcatInterface(ABC):
    @property
    @abstractmethod
    def attack_mode(self):
        pass

    @attack_mode.setter
    @abstractmethod
    def attack_mode(self, value):
        pass

    @property
    @abstractmethod
    def backend_devices(self):
        pass

    @backend_devices.setter
    @abstractmethod
    def backend_devices(self, value):
        pass

    @property
    @abstractmethod
    def backend_info(self):
        pass

    @backend_info.setter
    @abstractmethod
    def backend_info(self, value):
        pass

    @property
    @abstractmethod
    def backend_vector_width(self):
        pass

    @backend_vector_width.setter
    @abstractmethod
    def backend_vector_width(self, value):
        pass

    @property
    @abstractmethod
    def benchmark(self):
        pass

    @benchmark.setter
    @abstractmethod
    def benchmark(self, value):
        pass

    @property
    @abstractmethod
    def benchmark_all(self):
        pass

    @benchmark_all.setter
    @abstractmethod
    def benchmark_all(self, value):
        pass

    @property
    @abstractmethod
    def bitmap_max(self):
        pass

    @bitmap_max.setter
    @abstractmethod
    def bitmap_max(self, value):
        pass

    @property
    @abstractmethod
    def bitmap_min(self):
        pass

    @bitmap_min.setter
    @abstractmethod
    def bitmap_min(self, value):
        pass

    @property
    @abstractmethod
    def brain_client(self):
        pass

    @brain_client.setter
    @abstractmethod
    def brain_client(self, value):
        pass

    @property
    @abstractmethod
    def brain_client_features(self):
        pass

    @brain_client_features.setter
    @abstractmethod
    def brain_client_features(self, value):
        pass

    @property
    @abstractmethod
    def brain_host(self):
        pass

    @brain_host.setter
    @abstractmethod
    def brain_host(self, value):
        pass

    @property
    @abstractmethod
    def brain_password(self):
        pass

    @brain_password.setter
    @abstractmethod
    def brain_password(self, value):
        pass

    @property
    @abstractmethod
    def brain_port(self):
        pass

    @brain_port.setter
    @abstractmethod
    def brain_port(self, value):
        pass

    @property
    @abstractmethod
    def brain_server(self):
        pass

    @brain_server.setter
    @abstractmethod
    def brain_server(self, value):
        pass

    @property
    @abstractmethod
    def brain_session(self):
        pass

    @brain_session.setter
    @abstractmethod
    def brain_session(self, value):
        pass

    @property
    @abstractmethod
    def brain_session_whitelist(self):
        pass

    @brain_session_whitelist.setter
    @abstractmethod
    def brain_session_whitelist(self, value):
        pass

    @property
    @abstractmethod
    def cpu_affinity(self):
        pass

    @cpu_affinity.setter
    @abstractmethod
    def cpu_affinity(self, value):
        pass

    @property
    @abstractmethod
    def custom_charset_1(self):
        pass

    @custom_charset_1.setter
    @abstractmethod
    def custom_charset_1(self, value):
        pass

    @property
    @abstractmethod
    def custom_charset_2(self):
        pass

    @custom_charset_2.setter
    @abstractmethod
    def custom_charset_2(self, value):
        pass

    @property
    @abstractmethod
    def custom_charset_3(self):
        pass

    @custom_charset_3.setter
    @abstractmethod
    def custom_charset_3(self, value):
        pass

    @property
    @abstractmethod
    def custom_charset_4(self):
        pass

    @custom_charset_4.setter
    @abstractmethod
    def custom_charset_4(self, value):
        pass

    @property
    @abstractmethod
    def debug_file(self):
        pass

    @debug_file.setter
    @abstractmethod
    def debug_file(self, value):
        pass

    @property
    @abstractmethod
    def debug_mode(self):
        pass

    @debug_mode.setter
    @abstractmethod
    def debug_mode(self, value):
        pass

    @property
    @abstractmethod
    def dict1(self):
        pass

    @dict1.setter
    @abstractmethod
    def dict1(self, value):
        pass

    @property
    @abstractmethod
    def dict2(self):
        pass

    @dict2.setter
    @abstractmethod
    def dict2(self, value):
        pass

    @abstractmethod
    def event_connect(self, callback, signal):
        pass

    @property
    @abstractmethod
    def event_types(self):
        pass

    @event_types.setter
    @abstractmethod
    def event_types(self, value):
        pass

    @property
    @abstractmethod
    def force(self):
        pass

    @force.setter
    @abstractmethod
    def force(self, value):
        pass

    @property
    @abstractmethod
    def hash(self):
        pass

    @hash.setter
    @abstractmethod
    def hash(self, value):
        pass

    @property
    @abstractmethod
    def hash_mode(self):
        pass

    @hash_mode.setter
    @abstractmethod
    def hash_mode(self, value):
        pass

    @property
    @abstractmethod
    def hashcat_list_hashmodes(self):
        pass

    @hashcat_list_hashmodes.setter
    @abstractmethod
    def hashcat_list_hashmodes(self, value):
        pass

    @property
    @abstractmethod
    def hashcat_session_bypass(self):
        pass

    @hashcat_session_bypass.setter
    @abstractmethod
    def hashcat_session_bypass(self, value):
        pass

    @property
    @abstractmethod
    def hashcat_session_checkpoint(self):
        pass

    @hashcat_session_checkpoint.setter
    @abstractmethod
    def hashcat_session_checkpoint(self, value):
        pass

    @abstractmethod
    def hashcat_session_init(self):
        pass

    @abstractmethod
    def hashcat_session_execute(self):
        pass

    @property
    @abstractmethod
    def hashcat_session_pause(self):
        pass

    @hashcat_session_pause.setter
    @abstractmethod
    def hashcat_session_pause(self, value):
        pass

    @property
    @abstractmethod
    def hashcat_session_quit(self):
        pass

    @hashcat_session_quit.setter
    @abstractmethod
    def hashcat_session_quit(self, value):
        pass

    @property
    @abstractmethod
    def hashcat_session_resume(self):
        pass

    @hashcat_session_resume.setter
    @abstractmethod
    def hashcat_session_resume(self, value):
        pass

    @property
    @abstractmethod
    def hashcat_status_get_log(self):
        pass

    @hashcat_status_get_log.setter
    @abstractmethod
    def hashcat_status_get_log(self, value):
        pass

    @property
    @abstractmethod
    def hashcat_status_get_status(self):
        pass

    @hashcat_status_get_status.setter
    @abstractmethod
    def hashcat_status_get_status(self, value):
        pass

    @property
    @abstractmethod
    def hex_charset(self):
        pass

    @hex_charset.setter
    @abstractmethod
    def hex_charset(self, value):
        pass

    @property
    @abstractmethod
    def hex_salt(self):
        pass

    @hex_salt.setter
    @abstractmethod
    def hex_salt(self, value):
        pass

    @property
    @abstractmethod
    def hex_wordlist(self):
        pass

    @hex_wordlist.setter
    @abstractmethod
    def hex_wordlist(self, value):
        pass

    @property
    @abstractmethod
    def hwmon_disable(self):
        pass

    @hwmon_disable.setter
    @abstractmethod
    def hwmon_disable(self, value):
        pass

    @property
    @abstractmethod
    def hwmon_temp_abort(self):
        pass

    @hwmon_temp_abort.setter
    @abstractmethod
    def hwmon_temp_abort(self, value):
        pass

    @property
    @abstractmethod
    def increment(self):
        pass

    @increment.setter
    @abstractmethod
    def increment(self, value):
        pass

    @property
    @abstractmethod
    def increment_max(self):
        pass

    @increment_max.setter
    @abstractmethod
    def increment_max(self, value):
        pass

    @property
    @abstractmethod
    def increment_min(self):
        pass

    @increment_min.setter
    @abstractmethod
    def increment_min(self, value):
        pass

    @property
    @abstractmethod
    def induction_dir(self):
        pass

    @induction_dir.setter
    @abstractmethod
    def induction_dir(self, value):
        pass

    @property
    @abstractmethod
    def keep_guessing(self):
        pass

    @keep_guessing.setter
    @abstractmethod
    def keep_guessing(self, value):
        pass

    @property
    @abstractmethod
    def kernel_accel(self):
        pass

    @kernel_accel.setter
    @abstractmethod
    def kernel_accel(self, value):
        pass

    @property
    @abstractmethod
    def kernel_loops(self):
        pass

    @kernel_loops.setter
    @abstractmethod
    def kernel_loops(self, value):
        pass

    @property
    @abstractmethod
    def keyspace(self):
        pass

    @keyspace.setter
    @abstractmethod
    def keyspace(self, value):
        pass

    @property
    @abstractmethod
    def left(self):
        pass

    @left.setter
    @abstractmethod
    def left(self, value):
        pass

    @property
    @abstractmethod
    def limit(self):
        pass

    @limit.setter
    @abstractmethod
    def limit(self, value):
        pass

    @property
    @abstractmethod
    def logfile_disable(self):
        pass

    @logfile_disable.setter
    @abstractmethod
    def logfile_disable(self, value):
        pass

    @property
    @abstractmethod
    def loopback(self):
        pass

    @loopback.setter
    @abstractmethod
    def loopback(self, value):
        pass

    @property
    @abstractmethod
    def machine_readable(self):
        pass

    @machine_readable.setter
    @abstractmethod
    def machine_readable(self, value):
        pass

    @property
    @abstractmethod
    def markov_classic(self):
        pass

    @markov_classic.setter
    @abstractmethod
    def markov_classic(self, value):
        pass

    @property
    @abstractmethod
    def markov_disable(self):
        pass

    @markov_disable.setter
    @abstractmethod
    def markov_disable(self, value):
        pass

    @property
    @abstractmethod
    def markov_hcstat2(self):
        pass

    @markov_hcstat2.setter
    @abstractmethod
    def markov_hcstat2(self, value):
        pass

    @property
    @abstractmethod
    def markov_threshold(self):
        pass

    @markov_threshold.setter
    @abstractmethod
    def markov_threshold(self, value):
        pass

    @property
    @abstractmethod
    def mask(self):
        pass

    @mask.setter
    @abstractmethod
    def mask(self, value):
        pass

    @property
    @abstractmethod
    def opencl_device_types(self):
        pass

    @opencl_device_types.setter
    @abstractmethod
    def opencl_device_types(self, value):
        pass

    @property
    @abstractmethod
    def optimized_kernel_enable(self):
        pass

    @optimized_kernel_enable.setter
    @abstractmethod
    def optimized_kernel_enable(self, value):
        pass

    @property
    @abstractmethod
    def outfile(self):
        pass

    @outfile.setter
    @abstractmethod
    def outfile(self, value):
        pass

    @property
    @abstractmethod
    def outfile_autohex(self):
        pass

    @outfile_autohex.setter
    @abstractmethod
    def outfile_autohex(self, value):
        pass

    @property
    @abstractmethod
    def outfile_check_dir(self):
        pass

    @outfile_check_dir.setter
    @abstractmethod
    def outfile_check_dir(self, value):
        pass

    @property
    @abstractmethod
    def outfile_check_timer(self):
        pass

    @outfile_check_timer.setter
    @abstractmethod
    def outfile_check_timer(self, value):
        pass

    @property
    @abstractmethod
    def outfile_format(self):
        pass

    @outfile_format.setter
    @abstractmethod
    def outfile_format(self, value):
        pass

    @property
    @abstractmethod
    def potfile_disable(self):
        pass

    @potfile_disable.setter
    @abstractmethod
    def potfile_disable(self, value):
        pass

    @property
    @abstractmethod
    def potfile_path(self):
        pass

    @potfile_path.setter
    @abstractmethod
    def potfile_path(self, value):
        pass

    @property
    @abstractmethod
    def progress_only(self):
        pass

    @progress_only.setter
    @abstractmethod
    def progress_only(self, value):
        pass

    @property
    @abstractmethod
    def quiet(self):
        pass

    @quiet.setter
    @abstractmethod
    def quiet(self, value):
        pass

    @property
    @abstractmethod
    def remove(self):
        pass

    @remove.setter
    @abstractmethod
    def remove(self, value):
        pass

    @property
    @abstractmethod
    def remove_timer(self):
        pass

    @remove_timer.setter
    @abstractmethod
    def remove_timer(self, value):
        pass

    @property
    @abstractmethod
    def reset(self):
        pass

    @reset.setter
    @abstractmethod
    def reset(self, value):
        pass

    @property
    @abstractmethod
    def restore(self):
        pass

    @restore.setter
    @abstractmethod
    def restore(self, value):
        pass

    @property
    @abstractmethod
    def restore_disable(self):
        pass

    @restore_disable.setter
    @abstractmethod
    def restore_disable(self, value):
        pass

    @property
    @abstractmethod
    def restore_file_path(self):
        pass

    @restore_file_path.setter
    @abstractmethod
    def restore_file_path(self, value):
        pass

    @property
    @abstractmethod
    def restore_timer(self):
        pass

    @restore_timer.setter
    @abstractmethod
    def restore_timer(self, value):
        pass

    @property
    @abstractmethod
    def rp_files_cnt(self):
        pass

    @rp_files_cnt.setter
    @abstractmethod
    def rp_files_cnt(self, value):
        pass

    @property
    @abstractmethod
    def rp_gen(self):
        pass

    @rp_gen.setter
    @abstractmethod
    def rp_gen(self, value):
        pass

    @property
    @abstractmethod
    def rp_gen_func_max(self):
        pass

    @rp_gen_func_max.setter
    @abstractmethod
    def rp_gen_func_max(self, value):
        pass

    @property
    @abstractmethod
    def rp_gen_func_min(self):
        pass

    @rp_gen_func_min.setter
    @abstractmethod
    def rp_gen_func_min(self, value):
        pass

    @property
    @abstractmethod
    def rp_gen_seed(self):
        pass

    @rp_gen_seed.setter
    @abstractmethod
    def rp_gen_seed(self, value):
        pass

    @property
    @abstractmethod
    def rule_buf_l(self):
        pass

    @rule_buf_l.setter
    @abstractmethod
    def rule_buf_l(self, value):
        pass

    @property
    @abstractmethod
    def rule_buf_r(self):
        pass

    @rule_buf_r.setter
    @abstractmethod
    def rule_buf_r(self, value):
        pass

    @property
    @abstractmethod
    def rules(self):
        pass

    @rules.setter
    @abstractmethod
    def rules(self, value):
        pass

    @property
    @abstractmethod
    def runtime(self):
        pass

    @runtime.setter
    @abstractmethod
    def runtime(self, value):
        pass

    @property
    @abstractmethod
    def scrypt_tmto(self):
        pass

    @scrypt_tmto.setter
    @abstractmethod
    def scrypt_tmto(self, value):
        pass

    @property
    @abstractmethod
    def segment_size(self):
        pass

    @segment_size.setter
    @abstractmethod
    def segment_size(self, value):
        pass

    @property
    @abstractmethod
    def separator(self):
        pass

    @separator.setter
    @abstractmethod
    def separator(self, value):
        pass

    @property
    @abstractmethod
    def session(self):
        pass

    @session.setter
    @abstractmethod
    def session(self, value):
        pass

    @property
    @abstractmethod
    def show(self):
        pass

    @show.setter
    @abstractmethod
    def show(self, value):
        pass

    @property
    @abstractmethod
    def skip(self):
        pass

    @skip.setter
    @abstractmethod
    def skip(self, value):
        pass

    @property
    @abstractmethod
    def soft_reset(self):
        pass

    @soft_reset.setter
    @abstractmethod
    def soft_reset(self, value):
        pass

    @property
    @abstractmethod
    def speed_only(self):
        pass

    @speed_only.setter
    @abstractmethod
    def speed_only(self, value):
        pass

    @property
    @abstractmethod
    def spin_damp(self):
        pass

    @spin_damp.setter
    @abstractmethod
    def spin_damp(self, value):
        pass

    @property
    @abstractmethod
    def status_get_brain_rx_all(self):
        pass

    @status_get_brain_rx_all.setter
    @abstractmethod
    def status_get_brain_rx_all(self, value):
        pass

    @property
    @abstractmethod
    def status_get_corespeed_dev(self):
        pass

    @status_get_corespeed_dev.setter
    @abstractmethod
    def status_get_corespeed_dev(self, value):
        pass

    @property
    @abstractmethod
    def status_get_cpt(self):
        pass

    @status_get_cpt.setter
    @abstractmethod
    def status_get_cpt(self, value):
        pass

    @property
    @abstractmethod
    def status_get_cpt_avg_day(self):
        pass

    @status_get_cpt_avg_day.setter
    @abstractmethod
    def status_get_cpt_avg_day(self, value):
        pass

    @property
    @abstractmethod
    def status_get_cpt_avg_hour(self):
        pass

    @status_get_cpt_avg_hour.setter
    @abstractmethod
    def status_get_cpt_avg_hour(self, value):
        pass

    @property
    @abstractmethod
    def status_get_cpt_avg_min(self):
        pass

    @status_get_cpt_avg_min.setter
    @abstractmethod
    def status_get_cpt_avg_min(self, value):
        pass

    @property
    @abstractmethod
    def status_get_cpt_cur_day(self):
        pass

    @status_get_cpt_cur_day.setter
    @abstractmethod
    def status_get_cpt_cur_day(self, value):
        pass

    @property
    @abstractmethod
    def status_get_cpt_cur_hour(self):
        pass

    @status_get_cpt_cur_hour.setter
    @abstractmethod
    def status_get_cpt_cur_hour(self, value):
        pass

    @property
    @abstractmethod
    def status_get_cpt_cur_min(self):
        pass

    @status_get_cpt_cur_min.setter
    @abstractmethod
    def status_get_cpt_cur_min(self, value):
        pass

    @property
    @abstractmethod
    def status_get_device_info_active(self):
        pass

    @status_get_device_info_active.setter
    @abstractmethod
    def status_get_device_info_active(self, value):
        pass

    @property
    @abstractmethod
    def status_get_device_info_cnt(self):
        pass

    @status_get_device_info_cnt.setter
    @abstractmethod
    def status_get_device_info_cnt(self, value):
        pass

    @property
    @abstractmethod
    def status_get_digests_cnt(self):
        pass

    @status_get_digests_cnt.setter
    @abstractmethod
    def status_get_digests_cnt(self, value):
        pass

    @property
    @abstractmethod
    def status_get_digests_done(self):
        pass

    @status_get_digests_done.setter
    @abstractmethod
    def status_get_digests_done(self, value):
        pass

    @property
    @abstractmethod
    def status_get_digests_percent(self):
        pass

    @status_get_digests_percent.setter
    @abstractmethod
    def status_get_digests_percent(self, value):
        pass

    @property
    @abstractmethod
    def status_get_exec_msec_all(self):
        pass

    @status_get_exec_msec_all.setter
    @abstractmethod
    def status_get_exec_msec_all(self, value):
        pass

    @property
    @abstractmethod
    def status_get_exec_msec_dev(self):
        pass

    @status_get_exec_msec_dev.setter
    @abstractmethod
    def status_get_exec_msec_dev(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_base(self):
        pass

    @status_get_guess_base.setter
    @abstractmethod
    def status_get_guess_base(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_base_count(self):
        pass

    @status_get_guess_base_count.setter
    @abstractmethod
    def status_get_guess_base_count(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_base_offset(self):
        pass

    @status_get_guess_base_offset.setter
    @abstractmethod
    def status_get_guess_base_offset(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_base_percent(self):
        pass

    @status_get_guess_base_percent.setter
    @abstractmethod
    def status_get_guess_base_percent(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_candidates_dev(self):
        pass

    @status_get_guess_candidates_dev.setter
    @abstractmethod
    def status_get_guess_candidates_dev(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_charset(self):
        pass

    @status_get_guess_charset.setter
    @abstractmethod
    def status_get_guess_charset(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_mask_length(self):
        pass

    @status_get_guess_mask_length.setter
    @abstractmethod
    def status_get_guess_mask_length(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_mod(self):
        pass

    @status_get_guess_mod.setter
    @abstractmethod
    def status_get_guess_mod(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_mod_count(self):
        pass

    @status_get_guess_mod_count.setter
    @abstractmethod
    def status_get_guess_mod_count(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_mod_offset(self):
        pass

    @status_get_guess_mod_offset.setter
    @abstractmethod
    def status_get_guess_mod_offset(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_mod_percent(self):
        pass

    @status_get_guess_mod_percent.setter
    @abstractmethod
    def status_get_guess_mod_percent(self, value):
        pass

    @property
    @abstractmethod
    def status_get_guess_mode(self):
        pass

    @status_get_guess_mode.setter
    @abstractmethod
    def status_get_guess_mode(self, value):
        pass

    @property
    @abstractmethod
    def status_get_hash_name(self):
        pass

    @status_get_hash_name.setter
    @abstractmethod
    def status_get_hash_name(self, value):
        pass

    @property
    @abstractmethod
    def status_get_hash_target(self):
        pass

    @status_get_hash_target.setter
    @abstractmethod
    def status_get_hash_target(self, value):
        pass

    @property
    @abstractmethod
    def status_get_hashes_msec_all(self):
        pass

    @status_get_hashes_msec_all.setter
    @abstractmethod
    def status_get_hashes_msec_all(self, value):
        pass

    @property
    @abstractmethod
    def status_get_hashes_msec_dev(self):
        pass

    @status_get_hashes_msec_dev.setter
    @abstractmethod
    def status_get_hashes_msec_dev(self, value):
        pass

    @property
    @abstractmethod
    def status_get_hashes_msec_dev_benchmark(self):
        pass

    @status_get_hashes_msec_dev_benchmark.setter
    @abstractmethod
    def status_get_hashes_msec_dev_benchmark(self, value):
        pass

    @property
    @abstractmethod
    def status_get_hwmon_dev(self):
        pass

    @status_get_hwmon_dev.setter
    @abstractmethod
    def status_get_hwmon_dev(self, value):
        pass

    @property
    @abstractmethod
    def status_get_memoryspeed_dev(self):
        pass

    @status_get_memoryspeed_dev.setter
    @abstractmethod
    def status_get_memoryspeed_dev(self, value):
        pass

    @property
    @abstractmethod
    def status_get_msec_paused(self):
        pass

    @status_get_msec_paused.setter
    @abstractmethod
    def status_get_msec_paused(self, value):
        pass

    @property
    @abstractmethod
    def status_get_msec_real(self):
        pass

    @status_get_msec_real.setter
    @abstractmethod
    def status_get_msec_real(self, value):
        pass

    @property
    @abstractmethod
    def status_get_msec_running(self):
        pass

    @status_get_msec_running.setter
    @abstractmethod
    def status_get_msec_running(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_cur(self):
        pass

    @status_get_progress_cur.setter
    @abstractmethod
    def status_get_progress_cur(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_cur_relative_skip(self):
        pass

    @status_get_progress_cur_relative_skip.setter
    @abstractmethod
    def status_get_progress_cur_relative_skip(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_dev(self):
        pass

    @status_get_progress_dev.setter
    @abstractmethod
    def status_get_progress_dev(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_done(self):
        pass

    @status_get_progress_done.setter
    @abstractmethod
    def status_get_progress_done(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_end(self):
        pass

    @status_get_progress_end.setter
    @abstractmethod
    def status_get_progress_end(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_end_relative_skip(self):
        pass

    @status_get_progress_end_relative_skip.setter
    @abstractmethod
    def status_get_progress_end_relative_skip(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_finished_percent(self):
        pass

    @status_get_progress_finished_percent.setter
    @abstractmethod
    def status_get_progress_finished_percent(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_ignore(self):
        pass

    @status_get_progress_ignore.setter
    @abstractmethod
    def status_get_progress_ignore(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_mode(self):
        pass

    @status_get_progress_mode.setter
    @abstractmethod
    def status_get_progress_mode(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_rejected(self):
        pass

    @status_get_progress_rejected.setter
    @abstractmethod
    def status_get_progress_rejected(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_rejected_percent(self):
        pass

    @status_get_progress_rejected_percent.setter
    @abstractmethod
    def status_get_progress_rejected_percent(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_restored(self):
        pass

    @status_get_progress_restored.setter
    @abstractmethod
    def status_get_progress_restored(self, value):
        pass

    @property
    @abstractmethod
    def status_get_progress_skip(self):
        pass

    @status_get_progress_skip.setter
    @abstractmethod
    def status_get_progress_skip(self, value):
        pass

    @property
    @abstractmethod
    def status_get_restore_percent(self):
        pass

    @status_get_restore_percent.setter
    @abstractmethod
    def status_get_restore_percent(self, value):
        pass

    @property
    @abstractmethod
    def status_get_restore_point(self):
        pass

    @status_get_restore_point.setter
    @abstractmethod
    def status_get_restore_point(self, value):
        pass

    @property
    @abstractmethod
    def status_get_restore_total(self):
        pass

    @status_get_restore_total.setter
    @abstractmethod
    def status_get_restore_total(self, value):
        pass

    @property
    @abstractmethod
    def status_get_runtime_msec_dev(self):
        pass

    @status_get_runtime_msec_dev.setter
    @abstractmethod
    def status_get_runtime_msec_dev(self, value):
        pass

    @property
    @abstractmethod
    def status_get_salts_cnt(self):
        pass

    @status_get_salts_cnt.setter
    @abstractmethod
    def status_get_salts_cnt(self, value):
        pass

    @property
    @abstractmethod
    def status_get_salts_done(self):
        pass

    @status_get_salts_done.setter
    @abstractmethod
    def status_get_salts_done(self, value):
        pass

    @property
    @abstractmethod
    def status_get_salts_percent(self):
        pass

    @status_get_salts_percent.setter
    @abstractmethod
    def status_get_salts_percent(self, value):
        pass

    @property
    @abstractmethod
    def status_get_session(self):
        pass

    @status_get_session.setter
    @abstractmethod
    def status_get_session(self, value):
        pass

    @property
    @abstractmethod
    def status_get_skipped_dev(self):
        pass

    @status_get_skipped_dev.setter
    @abstractmethod
    def status_get_skipped_dev(self, value):
        pass

    @property
    @abstractmethod
    def status_get_speed_sec_all(self):
        pass

    @status_get_speed_sec_all.setter
    @abstractmethod
    def status_get_speed_sec_all(self, value):
        pass

    @property
    @abstractmethod
    def status_get_speed_sec_dev(self):
        pass

    @status_get_speed_sec_dev.setter
    @abstractmethod
    def status_get_speed_sec_dev(self, value):
        pass

    @property
    @abstractmethod
    def status_get_status_number(self):
        pass

    @status_get_status_number.setter
    @abstractmethod
    def status_get_status_number(self, value):
        pass

    @abstractmethod
    def status_get_status_string(self):
        pass

    @property
    @abstractmethod
    def status_get_time_estimated_absolute(self):
        pass

    @status_get_time_estimated_absolute.setter
    @abstractmethod
    def status_get_time_estimated_absolute(self, value):
        pass

    @property
    @abstractmethod
    def status_get_time_estimated_relative(self):
        pass

    @status_get_time_estimated_relative.setter
    @abstractmethod
    def status_get_time_estimated_relative(self, value):
        pass

    @property
    @abstractmethod
    def status_get_time_started_absolute(self):
        pass

    @status_get_time_started_absolute.setter
    @abstractmethod
    def status_get_time_started_absolute(self, value):
        pass

    @property
    @abstractmethod
    def status_get_time_started_relative(self):
        pass

    @status_get_time_started_relative.setter
    @abstractmethod
    def status_get_time_started_relative(self, value):
        pass

    @property
    @abstractmethod
    def status_reset(self):
        pass

    @status_reset.setter
    @abstractmethod
    def status_reset(self, value):
        pass

    @property
    @abstractmethod
    def truecrypt_keyfiles(self):
        pass

    @truecrypt_keyfiles.setter
    @abstractmethod
    def truecrypt_keyfiles(self, value):
        pass

    @property
    @abstractmethod
    def usage(self):
        pass

    @usage.setter
    @abstractmethod
    def usage(self, value):
        pass

    @property
    @abstractmethod
    def username(self):
        pass

    @username.setter
    @abstractmethod
    def username(self, value):
        pass

    @property
    @abstractmethod
    def veracrypt_keyfiles(self):
        pass

    @veracrypt_keyfiles.setter
    @abstractmethod
    def veracrypt_keyfiles(self, value):
        pass

    @property
    @abstractmethod
    def veracrypt_pim_start(self):
        pass

    @veracrypt_pim_start.setter
    @abstractmethod
    def veracrypt_pim_start(self, value):
        pass

    @property
    @abstractmethod
    def veracrypt_pim_stop(self):
        pass

    @veracrypt_pim_stop.setter
    @abstractmethod
    def veracrypt_pim_stop(self, value):
        pass

    @property
    @abstractmethod
    def workload_profile(self):
        pass

    @workload_profile.setter
    @abstractmethod
    def workload_profile(self, value):
        pass

    @abstractmethod
    def get_backend_devices_info(self):
        pass
