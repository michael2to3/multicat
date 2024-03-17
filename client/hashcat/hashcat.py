from .hashcat_interface import HashcatInterface
from pyhashcat import Hashcat as Cat


class Hashcat(HashcatInterface):
    def __init__(self, instance=Cat()):
        self._instance = instance

    @property
    def attack_mode(self):
        return self._instance.attack_mode

    @attack_mode.setter
    def attack_mode(self, value):
        self._instance.attack_mode = value

    @property
    def backend_devices(self):
        return self._instance.backend_devices

    @backend_devices.setter
    def backend_devices(self, value):
        self._instance.backend_devices = value

    @property
    def backend_info(self):
        return self._instance.backend_info

    @backend_info.setter
    def backend_info(self, value):
        self._instance.backend_info = value

    @property
    def backend_vector_width(self):
        return self._instance.backend_vector_width

    @backend_vector_width.setter
    def backend_vector_width(self, value):
        self._instance.backend_vector_width = value

    @property
    def benchmark(self):
        return self._instance.benchmark

    @benchmark.setter
    def benchmark(self, value):
        self._instance.benchmark = value

    @property
    def benchmark_all(self):
        return self._instance.benchmark_all

    @benchmark_all.setter
    def benchmark_all(self, value):
        self._instance.benchmark_all = value

    @property
    def bitmap_max(self):
        return self._instance.bitmap_max

    @bitmap_max.setter
    def bitmap_max(self, value):
        self._instance.bitmap_max = value

    @property
    def bitmap_min(self):
        return self._instance.bitmap_min

    @bitmap_min.setter
    def bitmap_min(self, value):
        self._instance.bitmap_min = value

    @property
    def brain_client(self):
        return self._instance.brain_client

    @brain_client.setter
    def brain_client(self, value):
        self._instance.brain_client = value

    @property
    def brain_client_features(self):
        return self._instance.brain_client_features

    @brain_client_features.setter
    def brain_client_features(self, value):
        self._instance.brain_client_features = value

    @property
    def brain_host(self):
        return self._instance.brain_host

    @brain_host.setter
    def brain_host(self, value):
        self._instance.brain_host = value

    @property
    def brain_password(self):
        return self._instance.brain_password

    @brain_password.setter
    def brain_password(self, value):
        self._instance.brain_password = value

    @property
    def brain_port(self):
        return self._instance.brain_port

    @brain_port.setter
    def brain_port(self, value):
        self._instance.brain_port = value

    @property
    def brain_server(self):
        return self._instance.brain_server

    @brain_server.setter
    def brain_server(self, value):
        self._instance.brain_server = value

    @property
    def brain_session(self):
        return self._instance.brain_session

    @brain_session.setter
    def brain_session(self, value):
        self._instance.brain_session = value

    @property
    def brain_session_whitelist(self):
        return self._instance.brain_session_whitelist

    @brain_session_whitelist.setter
    def brain_session_whitelist(self, value):
        self._instance.brain_session_whitelist = value

    @property
    def cpu_affinity(self):
        return self._instance.cpu_affinity

    @cpu_affinity.setter
    def cpu_affinity(self, value):
        self._instance.cpu_affinity = value

    @property
    def custom_charset_1(self):
        return self._instance.custom_charset_1

    @custom_charset_1.setter
    def custom_charset_1(self, value):
        self._instance.custom_charset_1 = value

    @property
    def custom_charset_2(self):
        return self._instance.custom_charset_2

    @custom_charset_2.setter
    def custom_charset_2(self, value):
        self._instance.custom_charset_2 = value

    @property
    def custom_charset_3(self):
        return self._instance.custom_charset_3

    @custom_charset_3.setter
    def custom_charset_3(self, value):
        self._instance.custom_charset_3 = value

    @property
    def custom_charset_4(self):
        return self._instance.custom_charset_4

    @custom_charset_4.setter
    def custom_charset_4(self, value):
        self._instance.custom_charset_4 = value

    @property
    def debug_file(self):
        return self._instance.debug_file

    @debug_file.setter
    def debug_file(self, value):
        self._instance.debug_file = value

    @property
    def debug_mode(self):
        return self._instance.debug_mode

    @debug_mode.setter
    def debug_mode(self, value):
        self._instance.debug_mode = value

    @property
    def dict1(self):
        return self._instance.dict1

    @dict1.setter
    def dict1(self, value):
        self._instance.dict1 = value

    @property
    def dict2(self):
        return self._instance.dict2

    @dict2.setter
    def dict2(self, value):
        self._instance.dict2 = value

    def event_connect(self, callback, signal):
        pass

    @property
    def event_types(self):
        return self._instance.event_types

    @event_types.setter
    def event_types(self, value):
        self._instance.event_types = value

    @property
    def force(self):
        return self._instance.force

    @force.setter
    def force(self, value):
        self._instance.force = value

    @property
    def hash(self):
        return self._instance.hash

    @hash.setter
    def hash(self, value):
        self._instance.hash = value

    @property
    def hash_mode(self):
        return self._instance.hash_mode

    @hash_mode.setter
    def hash_mode(self, value):
        self._instance.hash_mode = value

    @property
    def hashcat_list_hashmodes(self):
        return self._instance.hashcat_list_hashmodes

    @hashcat_list_hashmodes.setter
    def hashcat_list_hashmodes(self, value):
        self._instance.hashcat_list_hashmodes = value

    @property
    def hashcat_session_bypass(self):
        return self._instance.hashcat_session_bypass

    @hashcat_session_bypass.setter
    def hashcat_session_bypass(self, value):
        self._instance.hashcat_session_bypass = value

    @property
    def hashcat_session_checkpoint(self):
        return self._instance.hashcat_session_checkpoint

    @hashcat_session_checkpoint.setter
    def hashcat_session_checkpoint(self, value):
        self._instance.hashcat_session_checkpoint = value

    def hashcat_session_execute(self):
        pass

    @property
    def hashcat_session_pause(self):
        return self._instance.hashcat_session_pause

    @hashcat_session_pause.setter
    def hashcat_session_pause(self, value):
        self._instance.hashcat_session_pause = value

    @property
    def hashcat_session_quit(self):
        return self._instance.hashcat_session_quit

    @hashcat_session_quit.setter
    def hashcat_session_quit(self, value):
        self._instance.hashcat_session_quit = value

    @property
    def hashcat_session_resume(self):
        return self._instance.hashcat_session_resume

    @hashcat_session_resume.setter
    def hashcat_session_resume(self, value):
        self._instance.hashcat_session_resume = value

    @property
    def hashcat_status_get_log(self):
        return self._instance.hashcat_status_get_log

    @hashcat_status_get_log.setter
    def hashcat_status_get_log(self, value):
        self._instance.hashcat_status_get_log = value

    @property
    def hashcat_status_get_status(self):
        return self._instance.hashcat_status_get_status

    @hashcat_status_get_status.setter
    def hashcat_status_get_status(self, value):
        self._instance.hashcat_status_get_status = value

    @property
    def hex_charset(self):
        return self._instance.hex_charset

    @hex_charset.setter
    def hex_charset(self, value):
        self._instance.hex_charset = value

    @property
    def hex_salt(self):
        return self._instance.hex_salt

    @hex_salt.setter
    def hex_salt(self, value):
        self._instance.hex_salt = value

    @property
    def hex_wordlist(self):
        return self._instance.hex_wordlist

    @hex_wordlist.setter
    def hex_wordlist(self, value):
        self._instance.hex_wordlist = value

    @property
    def hwmon_disable(self):
        return self._instance.hwmon_disable

    @hwmon_disable.setter
    def hwmon_disable(self, value):
        self._instance.hwmon_disable = value

    @property
    def hwmon_temp_abort(self):
        return self._instance.hwmon_temp_abort

    @hwmon_temp_abort.setter
    def hwmon_temp_abort(self, value):
        self._instance.hwmon_temp_abort = value

    @property
    def increment(self):
        return self._instance.increment

    @increment.setter
    def increment(self, value):
        self._instance.increment = value

    @property
    def increment_max(self):
        return self._instance.increment_max

    @increment_max.setter
    def increment_max(self, value):
        self._instance.increment_max = value

    @property
    def increment_min(self):
        return self._instance.increment_min

    @increment_min.setter
    def increment_min(self, value):
        self._instance.increment_min = value

    @property
    def induction_dir(self):
        return self._instance.induction_dir

    @induction_dir.setter
    def induction_dir(self, value):
        self._instance.induction_dir = value

    @property
    def keep_guessing(self):
        return self._instance.keep_guessing

    @keep_guessing.setter
    def keep_guessing(self, value):
        self._instance.keep_guessing = value

    @property
    def kernel_accel(self):
        return self._instance.kernel_accel

    @kernel_accel.setter
    def kernel_accel(self, value):
        self._instance.kernel_accel = value

    @property
    def kernel_loops(self):
        return self._instance.kernel_loops

    @kernel_loops.setter
    def kernel_loops(self, value):
        self._instance.kernel_loops = value

    @property
    def keyspace(self):
        return self._instance.keyspace

    @keyspace.setter
    def keyspace(self, value):
        self._instance.keyspace = value

    @property
    def left(self):
        return self._instance.left

    @left.setter
    def left(self, value):
        self._instance.left = value

    @property
    def limit(self):
        return self._instance.limit

    @limit.setter
    def limit(self, value):
        self._instance.limit = value

    @property
    def logfile_disable(self):
        return self._instance.logfile_disable

    @logfile_disable.setter
    def logfile_disable(self, value):
        self._instance.logfile_disable = value

    @property
    def loopback(self):
        return self._instance.loopback

    @loopback.setter
    def loopback(self, value):
        self._instance.loopback = value

    @property
    def machine_readable(self):
        return self._instance.machine_readable

    @machine_readable.setter
    def machine_readable(self, value):
        self._instance.machine_readable = value

    @property
    def markov_classic(self):
        return self._instance.markov_classic

    @markov_classic.setter
    def markov_classic(self, value):
        self._instance.markov_classic = value

    @property
    def markov_disable(self):
        return self._instance.markov_disable

    @markov_disable.setter
    def markov_disable(self, value):
        self._instance.markov_disable = value

    @property
    def markov_hcstat2(self):
        return self._instance.markov_hcstat2

    @markov_hcstat2.setter
    def markov_hcstat2(self, value):
        self._instance.markov_hcstat2 = value

    @property
    def markov_threshold(self):
        return self._instance.markov_threshold

    @markov_threshold.setter
    def markov_threshold(self, value):
        self._instance.markov_threshold = value

    @property
    def mask(self):
        return self._instance.mask

    @mask.setter
    def mask(self, value):
        self._instance.mask = value

    @property
    def opencl_device_types(self):
        return self._instance.opencl_device_types

    @opencl_device_types.setter
    def opencl_device_types(self, value):
        self._instance.opencl_device_types = value

    @property
    def optimized_kernel_enable(self):
        return self._instance.optimized_kernel_enable

    @optimized_kernel_enable.setter
    def optimized_kernel_enable(self, value):
        self._instance.optimized_kernel_enable = value

    @property
    def outfile(self):
        return self._instance.outfile

    @outfile.setter
    def outfile(self, value):
        self._instance.outfile = value

    @property
    def outfile_autohex(self):
        return self._instance.outfile_autohex

    @outfile_autohex.setter
    def outfile_autohex(self, value):
        self._instance.outfile_autohex = value

    @property
    def outfile_check_dir(self):
        return self._instance.outfile_check_dir

    @outfile_check_dir.setter
    def outfile_check_dir(self, value):
        self._instance.outfile_check_dir = value

    @property
    def outfile_check_timer(self):
        return self._instance.outfile_check_timer

    @outfile_check_timer.setter
    def outfile_check_timer(self, value):
        self._instance.outfile_check_timer = value

    @property
    def outfile_format(self):
        return self._instance.outfile_format

    @outfile_format.setter
    def outfile_format(self, value):
        self._instance.outfile_format = value

    @property
    def potfile_disable(self):
        return self._instance.potfile_disable

    @potfile_disable.setter
    def potfile_disable(self, value):
        self._instance.potfile_disable = value

    @property
    def potfile_path(self):
        return self._instance.potfile_path

    @potfile_path.setter
    def potfile_path(self, value):
        self._instance.potfile_path = value

    @property
    def progress_only(self):
        return self._instance.progress_only

    @progress_only.setter
    def progress_only(self, value):
        self._instance.progress_only = value

    @property
    def quiet(self):
        return self._instance.quiet

    @quiet.setter
    def quiet(self, value):
        self._instance.quiet = value

    @property
    def remove(self):
        return self._instance.remove

    @remove.setter
    def remove(self, value):
        self._instance.remove = value

    @property
    def remove_timer(self):
        return self._instance.remove_timer

    @remove_timer.setter
    def remove_timer(self, value):
        self._instance.remove_timer = value

    @property
    def reset(self):
        return self._instance.reset

    @reset.setter
    def reset(self, value):
        self._instance.reset = value

    @property
    def restore(self):
        return self._instance.restore

    @restore.setter
    def restore(self, value):
        self._instance.restore = value

    @property
    def restore_disable(self):
        return self._instance.restore_disable

    @restore_disable.setter
    def restore_disable(self, value):
        self._instance.restore_disable = value

    @property
    def restore_file_path(self):
        return self._instance.restore_file_path

    @restore_file_path.setter
    def restore_file_path(self, value):
        self._instance.restore_file_path = value

    @property
    def restore_timer(self):
        return self._instance.restore_timer

    @restore_timer.setter
    def restore_timer(self, value):
        self._instance.restore_timer = value

    @property
    def rp_files_cnt(self):
        return self._instance.rp_files_cnt

    @rp_files_cnt.setter
    def rp_files_cnt(self, value):
        self._instance.rp_files_cnt = value

    @property
    def rp_gen(self):
        return self._instance.rp_gen

    @rp_gen.setter
    def rp_gen(self, value):
        self._instance.rp_gen = value

    @property
    def rp_gen_func_max(self):
        return self._instance.rp_gen_func_max

    @rp_gen_func_max.setter
    def rp_gen_func_max(self, value):
        self._instance.rp_gen_func_max = value

    @property
    def rp_gen_func_min(self):
        return self._instance.rp_gen_func_min

    @rp_gen_func_min.setter
    def rp_gen_func_min(self, value):
        self._instance.rp_gen_func_min = value

    @property
    def rp_gen_seed(self):
        return self._instance.rp_gen_seed

    @rp_gen_seed.setter
    def rp_gen_seed(self, value):
        self._instance.rp_gen_seed = value

    @property
    def rule_buf_l(self):
        return self._instance.rule_buf_l

    @rule_buf_l.setter
    def rule_buf_l(self, value):
        self._instance.rule_buf_l = value

    @property
    def rule_buf_r(self):
        return self._instance.rule_buf_r

    @rule_buf_r.setter
    def rule_buf_r(self, value):
        self._instance.rule_buf_r = value

    @property
    def rules(self):
        return self._instance.rules

    @rules.setter
    def rules(self, value):
        self._instance.rules = value

    @property
    def runtime(self):
        return self._instance.runtime

    @runtime.setter
    def runtime(self, value):
        self._instance.runtime = value

    @property
    def scrypt_tmto(self):
        return self._instance.scrypt_tmto

    @scrypt_tmto.setter
    def scrypt_tmto(self, value):
        self._instance.scrypt_tmto = value

    @property
    def segment_size(self):
        return self._instance.segment_size

    @segment_size.setter
    def segment_size(self, value):
        self._instance.segment_size = value

    @property
    def separator(self):
        return self._instance.separator

    @separator.setter
    def separator(self, value):
        self._instance.separator = value

    @property
    def session(self):
        return self._instance.session

    @session.setter
    def session(self, value):
        self._instance.session = value

    @property
    def show(self):
        return self._instance.show

    @show.setter
    def show(self, value):
        self._instance.show = value

    @property
    def skip(self):
        return self._instance.skip

    @skip.setter
    def skip(self, value):
        self._instance.skip = value

    @property
    def soft_reset(self):
        return self._instance.soft_reset

    @soft_reset.setter
    def soft_reset(self, value):
        self._instance.soft_reset = value

    @property
    def speed_only(self):
        return self._instance.speed_only

    @speed_only.setter
    def speed_only(self, value):
        self._instance.speed_only = value

    @property
    def spin_damp(self):
        return self._instance.spin_damp

    @spin_damp.setter
    def spin_damp(self, value):
        self._instance.spin_damp = value

    @property
    def status_get_brain_rx_all(self):
        return self._instance.status_get_brain_rx_all

    @status_get_brain_rx_all.setter
    def status_get_brain_rx_all(self, value):
        self._instance.status_get_brain_rx_all = value

    @property
    def status_get_corespeed_dev(self):
        return self._instance.status_get_corespeed_dev

    @status_get_corespeed_dev.setter
    def status_get_corespeed_dev(self, value):
        self._instance.status_get_corespeed_dev = value

    @property
    def status_get_cpt(self):
        return self._instance.status_get_cpt

    @status_get_cpt.setter
    def status_get_cpt(self, value):
        self._instance.status_get_cpt = value

    @property
    def status_get_cpt_avg_day(self):
        return self._instance.status_get_cpt_avg_day

    @status_get_cpt_avg_day.setter
    def status_get_cpt_avg_day(self, value):
        self._instance.status_get_cpt_avg_day = value

    @property
    def status_get_cpt_avg_hour(self):
        return self._instance.status_get_cpt_avg_hour

    @status_get_cpt_avg_hour.setter
    def status_get_cpt_avg_hour(self, value):
        self._instance.status_get_cpt_avg_hour = value

    @property
    def status_get_cpt_avg_min(self):
        return self._instance.status_get_cpt_avg_min

    @status_get_cpt_avg_min.setter
    def status_get_cpt_avg_min(self, value):
        self._instance.status_get_cpt_avg_min = value

    @property
    def status_get_cpt_cur_day(self):
        return self._instance.status_get_cpt_cur_day

    @status_get_cpt_cur_day.setter
    def status_get_cpt_cur_day(self, value):
        self._instance.status_get_cpt_cur_day = value

    @property
    def status_get_cpt_cur_hour(self):
        return self._instance.status_get_cpt_cur_hour

    @status_get_cpt_cur_hour.setter
    def status_get_cpt_cur_hour(self, value):
        self._instance.status_get_cpt_cur_hour = value

    @property
    def status_get_cpt_cur_min(self):
        return self._instance.status_get_cpt_cur_min

    @status_get_cpt_cur_min.setter
    def status_get_cpt_cur_min(self, value):
        self._instance.status_get_cpt_cur_min = value

    @property
    def status_get_device_info_active(self):
        return self._instance.status_get_device_info_active

    @status_get_device_info_active.setter
    def status_get_device_info_active(self, value):
        self._instance.status_get_device_info_active = value

    @property
    def status_get_device_info_cnt(self):
        return self._instance.status_get_device_info_cnt

    @status_get_device_info_cnt.setter
    def status_get_device_info_cnt(self, value):
        self._instance.status_get_device_info_cnt = value

    @property
    def status_get_digests_cnt(self):
        return self._instance.status_get_digests_cnt

    @status_get_digests_cnt.setter
    def status_get_digests_cnt(self, value):
        self._instance.status_get_digests_cnt = value

    @property
    def status_get_digests_done(self):
        return self._instance.status_get_digests_done

    @status_get_digests_done.setter
    def status_get_digests_done(self, value):
        self._instance.status_get_digests_done = value

    @property
    def status_get_digests_percent(self):
        return self._instance.status_get_digests_percent

    @status_get_digests_percent.setter
    def status_get_digests_percent(self, value):
        self._instance.status_get_digests_percent = value

    @property
    def status_get_exec_msec_all(self):
        return self._instance.status_get_exec_msec_all

    @status_get_exec_msec_all.setter
    def status_get_exec_msec_all(self, value):
        self._instance.status_get_exec_msec_all = value

    @property
    def status_get_exec_msec_dev(self):
        return self._instance.status_get_exec_msec_dev

    @status_get_exec_msec_dev.setter
    def status_get_exec_msec_dev(self, value):
        self._instance.status_get_exec_msec_dev = value

    @property
    def status_get_guess_base(self):
        return self._instance.status_get_guess_base

    @status_get_guess_base.setter
    def status_get_guess_base(self, value):
        self._instance.status_get_guess_base = value

    @property
    def status_get_guess_base_count(self):
        return self._instance.status_get_guess_base_count

    @status_get_guess_base_count.setter
    def status_get_guess_base_count(self, value):
        self._instance.status_get_guess_base_count = value

    @property
    def status_get_guess_base_offset(self):
        return self._instance.status_get_guess_base_offset

    @status_get_guess_base_offset.setter
    def status_get_guess_base_offset(self, value):
        self._instance.status_get_guess_base_offset = value

    @property
    def status_get_guess_base_percent(self):
        return self._instance.status_get_guess_base_percent

    @status_get_guess_base_percent.setter
    def status_get_guess_base_percent(self, value):
        self._instance.status_get_guess_base_percent = value

    @property
    def status_get_guess_candidates_dev(self):
        return self._instance.status_get_guess_candidates_dev

    @status_get_guess_candidates_dev.setter
    def status_get_guess_candidates_dev(self, value):
        self._instance.status_get_guess_candidates_dev = value

    @property
    def status_get_guess_charset(self):
        return self._instance.status_get_guess_charset

    @status_get_guess_charset.setter
    def status_get_guess_charset(self, value):
        self._instance.status_get_guess_charset = value

    @property
    def status_get_guess_mask_length(self):
        return self._instance.status_get_guess_mask_length

    @status_get_guess_mask_length.setter
    def status_get_guess_mask_length(self, value):
        self._instance.status_get_guess_mask_length = value

    @property
    def status_get_guess_mod(self):
        return self._instance.status_get_guess_mod

    @status_get_guess_mod.setter
    def status_get_guess_mod(self, value):
        self._instance.status_get_guess_mod = value

    @property
    def status_get_guess_mod_count(self):
        return self._instance.status_get_guess_mod_count

    @status_get_guess_mod_count.setter
    def status_get_guess_mod_count(self, value):
        self._instance.status_get_guess_mod_count = value

    @property
    def status_get_guess_mod_offset(self):
        return self._instance.status_get_guess_mod_offset

    @status_get_guess_mod_offset.setter
    def status_get_guess_mod_offset(self, value):
        self._instance.status_get_guess_mod_offset = value

    @property
    def status_get_guess_mod_percent(self):
        return self._instance.status_get_guess_mod_percent

    @status_get_guess_mod_percent.setter
    def status_get_guess_mod_percent(self, value):
        self._instance.status_get_guess_mod_percent = value

    @property
    def status_get_guess_mode(self):
        return self._instance.status_get_guess_mode

    @status_get_guess_mode.setter
    def status_get_guess_mode(self, value):
        self._instance.status_get_guess_mode = value

    @property
    def status_get_hash_name(self):
        return self._instance.status_get_hash_name

    @status_get_hash_name.setter
    def status_get_hash_name(self, value):
        self._instance.status_get_hash_name = value

    @property
    def status_get_hash_target(self):
        return self._instance.status_get_hash_target

    @status_get_hash_target.setter
    def status_get_hash_target(self, value):
        self._instance.status_get_hash_target = value

    @property
    def status_get_hashes_msec_all(self):
        return self._instance.status_get_hashes_msec_all

    @status_get_hashes_msec_all.setter
    def status_get_hashes_msec_all(self, value):
        self._instance.status_get_hashes_msec_all = value

    @property
    def status_get_hashes_msec_dev(self):
        return self._instance.status_get_hashes_msec_dev

    @status_get_hashes_msec_dev.setter
    def status_get_hashes_msec_dev(self, value):
        self._instance.status_get_hashes_msec_dev = value

    @property
    def status_get_hashes_msec_dev_benchmark(self):
        return self._instance.status_get_hashes_msec_dev_benchmark

    @status_get_hashes_msec_dev_benchmark.setter
    def status_get_hashes_msec_dev_benchmark(self, value):
        self._instance.status_get_hashes_msec_dev_benchmark = value

    @property
    def status_get_hwmon_dev(self):
        return self._instance.status_get_hwmon_dev

    @status_get_hwmon_dev.setter
    def status_get_hwmon_dev(self, value):
        self._instance.status_get_hwmon_dev = value

    @property
    def status_get_memoryspeed_dev(self):
        return self._instance.status_get_memoryspeed_dev

    @status_get_memoryspeed_dev.setter
    def status_get_memoryspeed_dev(self, value):
        self._instance.status_get_memoryspeed_dev = value

    @property
    def status_get_msec_paused(self):
        return self._instance.status_get_msec_paused

    @status_get_msec_paused.setter
    def status_get_msec_paused(self, value):
        self._instance.status_get_msec_paused = value

    @property
    def status_get_msec_real(self):
        return self._instance.status_get_msec_real

    @status_get_msec_real.setter
    def status_get_msec_real(self, value):
        self._instance.status_get_msec_real = value

    @property
    def status_get_msec_running(self):
        return self._instance.status_get_msec_running

    @status_get_msec_running.setter
    def status_get_msec_running(self, value):
        self._instance.status_get_msec_running = value

    @property
    def status_get_progress_cur(self):
        return self._instance.status_get_progress_cur

    @status_get_progress_cur.setter
    def status_get_progress_cur(self, value):
        self._instance.status_get_progress_cur = value

    @property
    def status_get_progress_cur_relative_skip(self):
        return self._instance.status_get_progress_cur_relative_skip

    @status_get_progress_cur_relative_skip.setter
    def status_get_progress_cur_relative_skip(self, value):
        self._instance.status_get_progress_cur_relative_skip = value

    @property
    def status_get_progress_dev(self):
        return self._instance.status_get_progress_dev

    @status_get_progress_dev.setter
    def status_get_progress_dev(self, value):
        self._instance.status_get_progress_dev = value

    @property
    def status_get_progress_done(self):
        return self._instance.status_get_progress_done

    @status_get_progress_done.setter
    def status_get_progress_done(self, value):
        self._instance.status_get_progress_done = value

    @property
    def status_get_progress_end(self):
        return self._instance.status_get_progress_end

    @status_get_progress_end.setter
    def status_get_progress_end(self, value):
        self._instance.status_get_progress_end = value

    @property
    def status_get_progress_end_relative_skip(self):
        return self._instance.status_get_progress_end_relative_skip

    @status_get_progress_end_relative_skip.setter
    def status_get_progress_end_relative_skip(self, value):
        self._instance.status_get_progress_end_relative_skip = value

    @property
    def status_get_progress_finished_percent(self):
        return self._instance.status_get_progress_finished_percent

    @status_get_progress_finished_percent.setter
    def status_get_progress_finished_percent(self, value):
        self._instance.status_get_progress_finished_percent = value

    @property
    def status_get_progress_ignore(self):
        return self._instance.status_get_progress_ignore

    @status_get_progress_ignore.setter
    def status_get_progress_ignore(self, value):
        self._instance.status_get_progress_ignore = value

    @property
    def status_get_progress_mode(self):
        return self._instance.status_get_progress_mode

    @status_get_progress_mode.setter
    def status_get_progress_mode(self, value):
        self._instance.status_get_progress_mode = value

    @property
    def status_get_progress_rejected(self):
        return self._instance.status_get_progress_rejected

    @status_get_progress_rejected.setter
    def status_get_progress_rejected(self, value):
        self._instance.status_get_progress_rejected = value

    @property
    def status_get_progress_rejected_percent(self):
        return self._instance.status_get_progress_rejected_percent

    @status_get_progress_rejected_percent.setter
    def status_get_progress_rejected_percent(self, value):
        self._instance.status_get_progress_rejected_percent = value

    @property
    def status_get_progress_restored(self):
        return self._instance.status_get_progress_restored

    @status_get_progress_restored.setter
    def status_get_progress_restored(self, value):
        self._instance.status_get_progress_restored = value

    @property
    def status_get_progress_skip(self):
        return self._instance.status_get_progress_skip

    @status_get_progress_skip.setter
    def status_get_progress_skip(self, value):
        self._instance.status_get_progress_skip = value

    @property
    def status_get_restore_percent(self):
        return self._instance.status_get_restore_percent

    @status_get_restore_percent.setter
    def status_get_restore_percent(self, value):
        self._instance.status_get_restore_percent = value

    @property
    def status_get_restore_point(self):
        return self._instance.status_get_restore_point

    @status_get_restore_point.setter
    def status_get_restore_point(self, value):
        self._instance.status_get_restore_point = value

    @property
    def status_get_restore_total(self):
        return self._instance.status_get_restore_total

    @status_get_restore_total.setter
    def status_get_restore_total(self, value):
        self._instance.status_get_restore_total = value

    @property
    def status_get_runtime_msec_dev(self):
        return self._instance.status_get_runtime_msec_dev

    @status_get_runtime_msec_dev.setter
    def status_get_runtime_msec_dev(self, value):
        self._instance.status_get_runtime_msec_dev = value

    @property
    def status_get_salts_cnt(self):
        return self._instance.status_get_salts_cnt

    @status_get_salts_cnt.setter
    def status_get_salts_cnt(self, value):
        self._instance.status_get_salts_cnt = value

    @property
    def status_get_salts_done(self):
        return self._instance.status_get_salts_done

    @status_get_salts_done.setter
    def status_get_salts_done(self, value):
        self._instance.status_get_salts_done = value

    @property
    def status_get_salts_percent(self):
        return self._instance.status_get_salts_percent

    @status_get_salts_percent.setter
    def status_get_salts_percent(self, value):
        self._instance.status_get_salts_percent = value

    @property
    def status_get_session(self):
        return self._instance.status_get_session

    @status_get_session.setter
    def status_get_session(self, value):
        self._instance.status_get_session = value

    @property
    def status_get_skipped_dev(self):
        return self._instance.status_get_skipped_dev

    @status_get_skipped_dev.setter
    def status_get_skipped_dev(self, value):
        self._instance.status_get_skipped_dev = value

    @property
    def status_get_speed_sec_all(self):
        return self._instance.status_get_speed_sec_all

    @status_get_speed_sec_all.setter
    def status_get_speed_sec_all(self, value):
        self._instance.status_get_speed_sec_all = value

    @property
    def status_get_speed_sec_dev(self):
        return self._instance.status_get_speed_sec_dev

    @status_get_speed_sec_dev.setter
    def status_get_speed_sec_dev(self, value):
        self._instance.status_get_speed_sec_dev = value

    @property
    def status_get_status_number(self):
        return self._instance.status_get_status_number

    @status_get_status_number.setter
    def status_get_status_number(self, value):
        self._instance.status_get_status_number = value

    def status_get_status_string(self):
        pass

    @property
    def status_get_time_estimated_absolute(self):
        return self._instance.status_get_time_estimated_absolute

    @status_get_time_estimated_absolute.setter
    def status_get_time_estimated_absolute(self, value):
        self._instance.status_get_time_estimated_absolute = value

    @property
    def status_get_time_estimated_relative(self):
        return self._instance.status_get_time_estimated_relative

    @status_get_time_estimated_relative.setter
    def status_get_time_estimated_relative(self, value):
        self._instance.status_get_time_estimated_relative = value

    @property
    def status_get_time_started_absolute(self):
        return self._instance.status_get_time_started_absolute

    @status_get_time_started_absolute.setter
    def status_get_time_started_absolute(self, value):
        self._instance.status_get_time_started_absolute = value

    @property
    def status_get_time_started_relative(self):
        return self._instance.status_get_time_started_relative

    @status_get_time_started_relative.setter
    def status_get_time_started_relative(self, value):
        self._instance.status_get_time_started_relative = value

    @property
    def status_reset(self):
        return self._instance.status_reset

    @status_reset.setter
    def status_reset(self, value):
        self._instance.status_reset = value

    @property
    def truecrypt_keyfiles(self):
        return self._instance.truecrypt_keyfiles

    @truecrypt_keyfiles.setter
    def truecrypt_keyfiles(self, value):
        self._instance.truecrypt_keyfiles = value

    @property
    def usage(self):
        return self._instance.usage

    @usage.setter
    def usage(self, value):
        self._instance.usage = value

    @property
    def username(self):
        return self._instance.username

    @username.setter
    def username(self, value):
        self._instance.username = value

    @property
    def veracrypt_keyfiles(self):
        return self._instance.veracrypt_keyfiles

    @veracrypt_keyfiles.setter
    def veracrypt_keyfiles(self, value):
        self._instance.veracrypt_keyfiles = value

    @property
    def veracrypt_pim_start(self):
        return self._instance.veracrypt_pim_start

    @veracrypt_pim_start.setter
    def veracrypt_pim_start(self, value):
        self._instance.veracrypt_pim_start = value

    @property
    def veracrypt_pim_stop(self):
        return self._instance.veracrypt_pim_stop

    @veracrypt_pim_stop.setter
    def veracrypt_pim_stop(self, value):
        self._instance.veracrypt_pim_stop = value

    @property
    def workload_profile(self):
        return self._instance.workload_profile

    @workload_profile.setter
    def workload_profile(self, value):
        self._instance.workload_profile = value
